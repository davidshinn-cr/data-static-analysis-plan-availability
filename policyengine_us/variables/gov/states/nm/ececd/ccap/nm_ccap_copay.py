from policyengine_us.model_api import *


class nm_ccap_copay(Variable):
    value_type = float
    entity = SPMUnit
    unit = USD
    definition_period = MONTH
    label = "New Mexico CCAP family copayment"
    defined_for = "nm_ccap_eligible"
    reference = (
        "https://www.nmececd.org/wp-content/uploads/2024/09/CCA-Co-payments-waived_rev1l.pdf#page=1",
        "https://www.nmlegis.gov/handouts/ALFC%20120825%20Item%208%20Policy%20Brief%20Child%20Care%20Update.pdf#page=2",
        "https://www.srca.nm.gov/parts/title08/08.015.0002.html",
    )

    def formula(spm_unit, period, parameters):
        p = parameters(period).gov.states.nm.ececd.ccap.copay
        # Three eras (LFC Policy Brief, Dec 9 2025, p.2):
        #   - copay.waived is true (2022-05-01 to 2023-06-30, and 2025-11-01
        #     onward under Universal Child Care): all copays waived -> $0.
        #   - copay.waived is false and period >= 2023-07-01: the copay was
        #     reinstated for families above 200% FPG under the published
        #     schedule (8.15.2.24 NMAC), now encoded under copay/schedule/.
        #   - copay.waived is false and period < 2022-05-01: the pre-2022 copay
        #     formula (8.15.2.13.B) is still not modeled, so schedule.in_effect
        #     is false there and the copay stays $0.
        if p.waived:
            return 0
        if not p.schedule.in_effect:
            return 0
        scheduled = spm_unit("nm_ccap_scheduled_copay", period)
        capped = min_(scheduled, p.schedule.max_amount)
        # 8.15.2.9 Priority 1/2: TANF families are not charged a copayment.
        if p.schedule.tanf_exempt:
            is_tanf = spm_unit("is_tanf_enrolled", period)
            return where(is_tanf, 0, capped)
        return capped
