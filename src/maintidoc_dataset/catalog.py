from __future__ import annotations

from dataclasses import dataclass
import re
from pathlib import Path


@dataclass(frozen=True)
class TopicMeta:
    system: str
    subsystem: str
    problem: str
    dtc_codes: tuple[str, ...] = ()


TOPICS: dict[int, TopicMeta] = {
    1: TopicMeta("HIGH_VOLTAGE", "battery_architecture", "architecture"),
    2: TopicMeta("HIGH_VOLTAGE", "battery_variants", "60ah_94ah"),
    3: TopicMeta("SAFETY", "high_voltage", "hv_safety"),
    4: TopicMeta("HIGH_VOLTAGE", "isolation", "isolation_fault", ("222814", "22280F", "21F0E3", "21F0E4")),
    5: TopicMeta("HIGH_VOLTAGE", "isolation", "intermittent_isolation", ("22280F", "21F0E3")),
    6: TopicMeta("HIGH_VOLTAGE", "sme_csc", "cell_supervision_fault", ("21F284", "21F13D", "21F153")),
    7: TopicMeta("HIGH_VOLTAGE", "cell_monitoring", "cell_undervoltage", ("21F241", "21F242", "21F243", "21F244", "21F245", "21F246", "21F247", "21F248", "22283B")),
    8: TopicMeta("HIGH_VOLTAGE", "battery_service", "end_of_service_failure"),
    9: TopicMeta("THERMAL", "battery_thermal", "hv_battery_thermal_management"),
    10: TopicMeta("ELECTRICAL", "battery_12v", "12v_hv_interaction", ("8040B9",)),
    11: TopicMeta("CHARGING", "KLE", "slow_ac_charging"),
    12: TopicMeta("CHARGING", "AC", "ac_charging_failure"),
    13: TopicMeta("CHARGING", "charge_port", "cable_lock_fault", ("805532", "805503")),
    14: TopicMeta("CHARGING", "charge_port", "emergency_release_fault"),
    15: TopicMeta("CHARGING", "ISTA", "charging_after_programming"),
    16: TopicMeta("CHARGING", "DC_fast_charge", "sme_fast_charge_fault", ("21F0D2", "21F153", "21F2A9")),
    17: TopicMeta("CHARGING", "charge_port", "charge_port_led", ("805532", "805503")),
    18: TopicMeta("ELECTRICAL", "battery_12v", "12v_charging_delay"),
    19: TopicMeta("EDRIVE", "EME", "drivetrain_fault", ("2228BF", "222852")),
    20: TopicMeta("EDRIVE", "rotor_sensor", "rotor_position_sensor", ("222011",)),
    21: TopicMeta("EDRIVE", "drive_readiness", "driving_readiness_failure", ("222851", "2228C0", "222761", "222011", "22230E", "222D27")),
    22: TopicMeta("EDRIVE", "parking_lock", "parking_lock_fault", ("222D25", "222D26", "222D29")),
    23: TopicMeta("EDRIVE", "motor_mount", "motor_mount_failure"),
    24: TopicMeta("EDRIVE", "motor_mount", "motor_mount_traction_loss"),
    25: TopicMeta("ELECTRICAL", "BDC", "black_screen_no_restart", ("D91C86",)),
    26: TopicMeta("THERMAL", "AC_compressor", "ac_compressor_fault", ("801252",)),
    27: TopicMeta("THERMAL", "heat_pump", "heat_pump_fault", ("801130",)),
    28: TopicMeta("THERMAL", "AC_sensor", "pressure_temperature_sensor", ("801295", "80112A")),
    29: TopicMeta("THERMAL", "heater_IHKA", "intermittent_heater", ("E70C3A", "E7147F", "E71482")),
    30: TopicMeta("THERMAL", "preconditioning", "preconditioning_after_charge"),
    31: TopicMeta("STEERING", "EPS", "no_assistance_startup"),
    32: TopicMeta("STEERING", "EPS", "sporadic_assistance_reduction"),
    33: TopicMeta("STEERING", "steering_column", "squeak_groan"),
    34: TopicMeta("BODY", "power_windows", "windows_inoperative"),
    35: TopicMeta("SAFETY", "airbag", "driver_airbag_fault", ("930904", "93090A")),
}


def number_from_filename(filename: str) -> int:
    match = re.match(r"(\d{2})_", Path(filename).name)
    if not match:
        raise ValueError(f"Nom de PDF inattendu: {filename}")
    return int(match.group(1))


def topic_for_filename(filename: str) -> TopicMeta:
    number = number_from_filename(filename)
    try:
        return TOPICS[number]
    except KeyError as exc:
        raise KeyError(f"Aucune métadonnée métier pour {filename}") from exc
