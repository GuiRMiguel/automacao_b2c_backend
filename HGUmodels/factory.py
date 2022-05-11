from .models.AskeyBROADCOM import HGU_AskeyBROADCOM
from .models.probe_MItraStarECNT.settingsProbe import HGU_MItraStarECNT_settingsProbe
from .models.probe_MItraStarECNT.wizardProbe import HGU_MItraStarECNT_wizardProbe
from .models.probe_MItraStarECNT.functionalProbe import HGU_MItraStarECNT_functionalProbe


from .models.probe_MItraStarBROADCOM.settingsProbe import HGU_MItraStarBROADCOM_settingsProbe
from .models.probe_MItraStarBROADCOM.wizardProbe import HGU_MItraStarBROADCOM_wizardProbe
from .models.probe_MItraStarBROADCOM.functionalProbe import HGU_MItraStarBROADCOM_functionalProbe


from .models.probe_AskeyECNT.settingsProbe import HGU_AskeyECNT_settingsProbe
from .models.probe_AskeyECNT.wizardProbe import HGU_AskeyECNT_wizardProbe
from .models.probe_AskeyECNT.functionalProbe import HGU_AskeyECNT_functionalProbe

from .models.probe_AskeyBroadcom.settingsProbe import HGU_AskeyBROADCOM_settingsProbe
from .models.probe_AskeyBroadcom.wizardProbe import HGU_AskeyBROADCOM_wizardProbe
from .models.probe_AskeyBroadcom.functionalProbe import HGU_AskeyBROADCOM_functionalProbe


class HGUModelFactory:
    @staticmethod
    def getHGU(probe, dict_result, model_name, username=None, password=None, address_ip=None, driver=None ):
        print(model_name)

        if model_name == 'HGU1_MItraStar_ECNT':
            if probe == 'settingsProbe':
                return HGU_MItraStarECNT_settingsProbe(address_ip, model_name, username, password, driver, dict_result)
            if probe == 'wizardProbe':
                return HGU_MItraStarECNT_wizardProbe(address_ip, model_name, username, password, driver, dict_result)
            if probe == 'functionalProbe':
                return HGU_MItraStarECNT_functionalProbe(address_ip, model_name, username, password, driver, dict_result)

          
        elif model_name == 'HGU4_MItraStar_BROADCOM':
            if probe == 'settingsProbe':
                return HGU_MItraStarBROADCOM_settingsProbe(address_ip, model_name, username, password, driver, dict_result)
            if probe == 'wizardProbe':
                return HGU_MItraStarBROADCOM_wizardProbe(address_ip, model_name, username, password, driver, dict_result)
            if probe == 'functionalProbe':
                return HGU_MItraStarBROADCOM_functionalProbe(address_ip, model_name, username, password, driver, dict_result)


        elif model_name == 'HGU2_Askey_ECNT':
            if probe == 'settingsProbe':
                return HGU_AskeyECNT_settingsProbe(address_ip, model_name, username, password, driver, dict_result)
            if probe == 'wizardProbe':
                return HGU_AskeyECNT_wizardProbe(address_ip, model_name, username, password, driver, dict_result)
            if probe == 'functionalProbe':
                return HGU_AskeyECNT_functionalProbe(address_ip, model_name, username, password, driver, dict_result)

        elif model_name == 'HGU3_Askey_BROADCOM':
            if probe == 'settingsProbe':
                return HGU_AskeyBROADCOM_settingsProbe(address_ip, model_name, username, password, driver, dict_result)
            if probe == 'wizardProbe':
                return HGU_AskeyBROADCOM_wizardProbe(address_ip, model_name, username, password, driver, dict_result)
            if probe == 'functionalProbe':
                return HGU_AskeyBROADCOM_functionalProbe(address_ip, model_name, username, password, driver, dict_result)
        else:
            return None
