from policyengine_us.model_api import *


class receives_tx_ccs_protective_services(Variable):
    value_type = bool
    entity = SPMUnit
    definition_period = MONTH
    label = "Receives Texas CCS protective services child care"
    defined_for = StateCode.TX
    reference = (
        "https://www.law.cornell.edu/regulations/texas/40-Tex-Admin-Code-SS-809-19"
    )
    documentation = (
        "Whether a child in the unit is receiving protective services child care "
        "on a DFPS referral. This is an input: the referral originates outside "
        "the household's own circumstances and cannot be derived from them."
    )
