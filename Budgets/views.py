from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Budget, PPO_Budget
from .serializers import BudgetSerializer, PPO_Serializer

        
def set_params(request, params):
    params['pcurent'].clear()
    params['pcurent'].update(params['pdefault'])
    for pl_elem in params['plist']:
        attr = request.GET.get(pl_elem,'none')
        if attr != 'none':
            params['pcurent'][pl_elem] = attr
            
class BudgetView(APIView):

    def get(self, request):
        # Проверяем атрибут "update" в GET-запросе
        update_attr = request.GET.get("update", False)
        
        budgets = Budget.objects.all()
        if not budgets.exists():
            set_params(request, budgets.options['params'])
            budgets.update_budget(budgets.options)
        else:
            if update_attr:
               set_params(request, budgets.options['params'])
               budgets.update_budget(budgets.options)
        serializer = BudgetSerializer(budgets, many=True)
        return Response({"БЮДЖЕТЫ": serializer.data})
        
class PPO_View(APIView):

    def get(self, request):
        # Проверяем атрибут "update" в GET-запросе
        update_attr = request.GET.get("update", False)
        
        budgets = Budget.objects.all()
        if not budgets.exists():
            #set_params(request, budgets.options['params'])
            budgets.update_budget(budgets.options)

        #print(budgets)
        PPOs = PPO_Budget.objects.all()
        if not PPOs.exists():
            set_params(request, PPOs.options['params'])
            PPOs.update_ppo(PPOs.options, budgets)
        else:
            if update_attr:
                set_params(request, PPOs.options['params'])
                PPOs.update_ppo(PPOs.options, budgets)
        serializer = PPO_Serializer(PPOs, many=True)
        return Response({"ПУБЛИЧНО-ПРАВОВЫЕ ОБРАЗОВАНИЯ": serializer.data})
