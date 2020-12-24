from django.db import models
from django.utils.translation import gettext_lazy as description
import datetime

class KBKStatus(models.TextChoices):
    ACTIVE              = "ACTIVE", description('Актуальная запись')
    ARCHIVE             = "ARCHIVE", description('Архивная запись')

class BudgetType(models.TextChoices):
    """Код типа бюджета"""
    OTHER = "00", description('Прочие бюджеты')
    FEDERAL = "01", description('Федеральный бюджет')
    SUBJECT = "02", description('Бюджет субъекта РФ')
    CAPITALS = "03", description('Бюджеты внутригородских МО г. Москвы и г. Санкт-Петербурга')
    CITY = "04", description('Бюджет городского округа')
    MUNICIPAL = "05", description('Бюджет муниципального района')
    PENSION = "06", description('Бюджет Пенсионного фонда РФ')
    FSS = "07", description('Бюджет ФСС РФ')
    FFOMS = "08", description('Бюджет ФФОМС')
    TFOMS = "09", description('Бюджет ТФОМС')
    LOCAL = "10", description('Бюджет поселения')
    URBANDISTRICT = "11", description('Бюджет городского округа с внутригородским делением')
    INNERCYTYAREA = "12", description('Бюджет внутригородского района городского округа')
    URBANSETTLEMENT = "13", description('Бюджет городского поселения')
    FEDERALCITY = "14", description('Бюджет города федерального значения')
    DISTRIBUTED = "98", description('Распределяемый доход')
    ORGANIZATION = "99", description('Доход организации (только для ПДИ)')

    __empty__ = description('Неопределённый')

class BudgetQS(models.QuerySet):

    budget_url = "http://budget.gov.ru/epbs/registry/7710568760-BUDGETS/data"
    
    # Определение настроек по умолчанию
    options = {'params':{'plist': [], 'pcurent': {}, 'pdefault': {}}, 'fields': {}, 'relations': {}}

    options['params']['plist'] = ['pageSize', 'pageNum', 'filterstatus', 'filtercode','filterparentcode']
    
    # По умолчанию фильтруем бюджеты Московской области
    options['params']['pdefault'] = { \
                                    'pageSize': '1000','pageNum': '1', \
                                    'sortField': "''",'filterstatus': 'ACTIVE', \
                                    'filtercode': '48______'  \
                                    }
    options['params']['pcurent'] = {}

    options['fields'] = { \
                        'code': 'code','name': 'name', \
                        'startdate': 'startdate','enddate':'enddate', \
                        'status': 'status','budgettype': 'budgtypecode',\
                        }
    options['relations'] =   {'parentcode': 'parentcode'}

    # Создаем или обновляем таблицу БД
    def update_budget(self, options):
        
        from .loadata import load_data_from
        
        budget_response_list = load_data_from(self.budget_url, options)
        budget_response_dict = {}
        
        # Создаем или обновляем основные записи таблицы БД
        print("Обновляем основные записи таблицы БД")
        for brl_elem in budget_response_list:
            if brl_elem['fields'] != None:
                budget_response_dict = brl_elem['fields']
                self.update_or_create(code=budget_response_dict['code'],defaults=budget_response_dict)
            else:
                budget_response_dict['code'] = options['params']['pcurent']['filtercode']
                budget_response_dict['name'] = 'Бюджет необнаружен'
                self.update_or_create(code=budget_response_dict['code'],defaults=budget_response_dict)
        print("Основные записи обновлены")
        
        # Определяем и обновляем связи внутри таблицы БД            
        print("Обновляем связи внутри таблицы БД")
        for brl_elem in budget_response_list:
            if brl_elem['relations'] != None:
                parent =  brl_elem['relations'].get('parentcode')
                if parent != '00000000' and parent != None and parent != brl_elem['fields']['code']:
                    parent = self._get_parent(parent, budget_response_list)
                    self.filter(code=brl_elem['fields']['code']).update(parentcode=parent)
                elif parent == brl_elem['fields']['code']:
                    parent = self.get(code=brl_elem['fields']['code'])
                    self.filter(code=brl_elem['fields']['code']).update(parentcode=parent)
            # else:
                # parent = self.get(code=budget_response_dict['code'])
                # self.filter(code=budget_response_dict['code']).update(parentcode=parent)
        print("Связи внутри таблицы обновлены")

    # Поиск предка по его коду со всеми его корнями
    def _get_parent(self, pcode, blist):
        print(f"Код: {pcode}") 
        if not self.filter(code__icontains=pcode).exists():
            opts = self.options.copy()
            opts['params']['pcurent']['filtercode'] = pcode
            self.update_budget(opts)
            parent = self.get(code=pcode)
        else:
            for bl_elem in blist:
                pc = bl_elem['relations'].get('parentcode')
                if bl_elem['fields']['code'] == pcode:
                    parent = self._get_parent(pc, blist)
                else:
                    parent = self.get(code=pcode)
            
        return parent
    
class BudgetManager(models.Manager):
    def get_queryset(self):
        return BudgetQS(self.model, using=self._db)
        
class Budget(models.Model):
    # guid                = models.CharField("Глобально-уникальный идентификатор записи", max_length=36)  # ! Не берем при импорте
    code                = models.CharField("Код", max_length=8, blank=False, null=False)
    name                = models.TextField("Полное наименование", max_length=2000, blank=False, null=False)
    parentcode          = models.ForeignKey('self', verbose_name="Вышестоящий бюджет", blank=True, null=True, on_delete=models.SET_NULL)
    startdate           = models.DateTimeField("Дата начала действия записи", blank=False, null=False, default=datetime.datetime.now)
    enddate             = models.DateTimeField("Дата окончания действия записи", blank=True, null=True)
    status              = models.CharField("Статус записи", max_length=7, choices=KBKStatus.choices, blank=False, null=False, default=KBKStatus.ACTIVE)
    budgettype          = models.CharField("Тип бюджета", max_length=2, choices=BudgetType.choices, blank=False, null=False, default=BudgetType.__empty__)
    class Meta:
        verbose_name    = 'Бюджеты' #'Справочник бюджетов'
        verbose_name_plural = 'Справочник бюджетов'#'Справочники бюджетов'
       
    objects = BudgetManager()

    def __str__(self):
        return f"{self.code}: {self.name}"

class PPO_QS(models.QuerySet):

    budget_url = "http://budget.gov.ru/epbs/registry/7710568760-BUDGETCLASGRBSFB/data"
    
    # Определение настроек по умолчанию
    options = {'params':{'plist': [], 'pcurent': {}, 'pdefault': {}}, 'fields': {}, 'relations': {}}

    options['params']['plist'] = ['pageSize', 'pageNum', 'budgetname', 'code','name','startdate','pponame','ppocode','year','enddate','stagename']
    options['params']['pdefault'] = {'pageSize': '100','pageNum': '1'}
    options['params']['pcurent'] = {}

    options['fields'] = { \
                        'code': 'code','name': 'name', \
                        'startdate': 'startdate','enddate':'enddate', \
                        'budgetname': 'budgetname' \
                        }
    options['relations'] =   {'budget': 'budgetname'}

    # Создаем или обновляем таблицу БД
    def update_ppo(self, options, budgets):
        
        from .loadata import load_data_from
        
        response_list = load_data_from(self.budget_url, options)
        response_dict = {}
        
        # Создаем или обновляем основные записи таблицы БД
        print("Обновляем основные записи таблицы БД")
        for rl_elem in response_list:
            response_dict = rl_elem['fields']
            response_dict['budgetname'] = response_dict['budgetname'].capitalize()
            self.update_or_create(code=response_dict['code'],defaults=response_dict)
        print("Основные записи обновлены")
        
        # Определяем и обновляем связи внутри таблицы БД            
        print("Обновляем связи внутри таблицы БД")
        for rl_elem in response_list:
                budgetname =  rl_elem['relations'].get('budget').capitalize()
                budgetname = budgets.get(name=budgetname)
                self.filter(code=rl_elem['fields']['code']).update(budget=budgetname)
        print("Связи внутри таблицы обновлены")
    
class PPO_Manager(models.Manager):
    def get_queryset(self):
        return PPO_QS(self.model, using=self._db)
        

class PPO_Budget(models.Model):
    """Справочник ППО по бюджетной классификации"""

    # guid                = models.CharField("Глобально-уникальный идентификатор записи", max_length=36)
    code                = models.CharField("Код", max_length=3, blank=False, null=False)  # ! если не будут пересекаться добавить: , unique=True
    name                = models.TextField("Сокращенное наименование", max_length=254, blank=True, null=True)
    budgetname          = models.TextField("Наименование бюджета", max_length=254, blank=True, null=True)
    startdate           = models.DateTimeField("Дата начала действия записи", blank=False, null=False, default=datetime.datetime.now)
    enddate             = models.DateTimeField("Дата окончания действия записи", null=True)
    budget              = models.ForeignKey(Budget, verbose_name="Бюджет", blank=True, null=True, on_delete=models.CASCADE)
    # tofkcode
    # ppocode
    #dateinclusion       = models.DateTimeField("Дата включения кода", blank=False, null=False, default=datetime.datetime.now)
    #dateexclusion       = models.DateTimeField("Дата исключения кода")
    # year                = models.DateField("Год")

    class Meta:
        verbose_name = 'Публично-правовые образования' #'Справочник главы по бюджетной классификации' # Публично-правовые образования 
        verbose_name_plural = 'Справочник ППО по бюджетной классификации'

    objects = PPO_Manager()

    def __str__(self):
        return f"{self.code}: {self.name}"

