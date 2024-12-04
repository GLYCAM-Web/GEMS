from gemsModules.common.services.workflow_manager import Service_Work_Flows_{{cookiecutter.gems_module}}
from gemsModules.common.services.workflow_manager import Service_Work_Flow_Order_{{cookiecutter.gems_module}}

from gemsModules.logging.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)


def get_Service_Work_Flows() -> Service_Work_Flows_{{cookiecutter.gems_module}}:
    """ Return services work Flows data
    """

    from gemsModules.{{cookiecutter.gems_module}}.services import marco
    from gemsModules.{{cookiecutter.gems_module}}.services import list_services
    from gemsModules.{{cookiecutter.gems_module}}.services import {{cookiecutter.service_name}}

    error_list = [ error ]
    list_services_list = [ list_services ]
    marco_list = [ marco ]
    {{cookiecutter.service_name}}_list = [ {{cookiecutter.service_name}} ]
    status_list = [ status ]
    
    Service_Work_Flows = Service_Work_Flows_{{cookiecutter.gems_module}}
    
    Service_Work_Flows.append(Service_Work_Flow_Order_{{cookiecutter.gems_module}}(
        "error", 
        error_list
            ))
    Service_Work_Flows.append(Service_Work_Flow_Order_{{cookiecutter.gems_module}}(
        "marco", 
        marco_list
            ))
    Service_Work_Flows.append(Service_Work_Flow_Order_{{cookiecutter.gems_module}}(
        "list_services", 
        list_services_list
            ))
    Service_Work_Flows.append(Service_Work_Flow_Order_{{cookiecutter.gems_module}}(
        "status", 
        status_list
            ))
    Service_Work_Flows.append(Service_Work_Flow_Order_{{cookiecutter.gems_module}}(
        "{{cookiecutter.service_name}}", 
        {{cookiecutter.service_name}}
            ))
    return Service_Work_Flows

def testme() :
    """ Test the workflows and get human-friendly output
        The part after the 'from' in the string'd module is removed for
        compatibility with multiple systems.
    >>> testme()
    -------------------------------------------------------------------------------
    -------------------------------------------------------------------------------
    The service work flows follow.
    -------------------------------------------------------------------------------
    Workflow type: marco
    Modules to call (services to run) :
        1 :  <module 'gemsModules.delegator.services.marco' 
    -------------------------------------------------------------------------------
    Workflow type: list_services
    Modules to call (services to run) :
        1 :  <module 'gemsModules.delegator.services.list_services' 
    -------------------------------------------------------------------------------
    -------------------------------------------------------------------------------
    """
    print("-------------------------------------------------------------------------------")
    print("-------------------------------------------------------------------------------")
    print("The service work flows follow.")
    print("-------------------------------------------------------------------------------")
    sep = 'from'
    for workflow in get_Service_Work_Flows():
        print("Workflow type: " + str(workflow.Service_Type))
        print("Modules to call (services to run) :")
        count=1
        for module in workflow.Operations_Order_List: 
          print("    " + str(count) + " :  " +  str(module).split(sep, 1)[0])
          count=count+1
        print("-------------------------------------------------------------------------------")
    print("-------------------------------------------------------------------------------")


if __name__ == "__main__":
    import doctest
    doctest.testmod()
