import os
import random
import sys
import threading
import time

try:
    import winsound
except ImportError:
    winsound = None


GREEN = "\033[92m"
RED = "\033[91m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
MAGENTA = "\033[95m"
BLUE = "\033[94m"
WHITE = "\033[97m"
DARK_GRAY = "\033[90m"
LIGHT_CYAN = "\033[1;36m"
LIGHT_RED = "\033[1;31m"
BOLD = "\033[1m"
RESET = "\033[0m"


# Чем меньше число, тем быстрее вывод.
SPEED_HEX_LINE = 0.003
SPEED_HEX_PAUSE = 0.05
SPEED_TYPING = 0.003
SPEED_EVENT_PAUSE = 0.08
CINEMATIC_INTRO = True
STORY_SPEED = 1.0
CONSOLE_ACCESS_INTRO = True
ACCESS_MENU_HOLD = 5.0
ADMIN_COMMAND_HOLD = 3.0
ADMIN_TYPING_INTERVAL = 0.080
SERVER_PROMPT_HOLD = 4.0
PATH_PROMPT_HOLD = 2.0
REALTIME_READ_HOLD = 1.0

CHAIN_CHANCE = 0.035
GLITCH_CHANCE = 0.025
SUPER_EVENT_FIRST_MIN = 25.0
SUPER_EVENT_FIRST_MAX = 50.0
SUPER_EVENT_MIN_DELAY = 70.0
SUPER_EVENT_MAX_DELAY = 160.0


PAUSED = threading.Event()
RUNNING = threading.Event()
RUNNING.set()

DEFCON = 0
DEFCON_DECAY_AT = time.monotonic() + 12.0
FLOW_MODE = "NORMAL"
FLOW_FACTOR = 1.0
FLOW_MODE_UNTIL = 0.0


MEM_BLOCKS = [0x7FFA, 0x8000, 0xC000, 0x0010, 0x7FFF, 0x0000, 0xFFFF, 0xD000]

SYSCALLS = [
    "NtCreateSection",
    "NtMapViewOfSection",
    "NtOpenProcess",
    "NtAllocateVirtualMemory",
    "NtProtectVirtualMemory",
    "NtQuerySystemInformation",
    "NtUserInstallInputHook",
]

MODULES = [
    "corekrnl.sys",
    "hal.dll",
    "gfxk.sys",
    "ntcore.dll",
    "netbus.sys",
    "authsvc.bin",
    "idvault.dll",
    "integrity.mod",
]

KERNEL_PANICS = [
    "CRITICAL_STRUCTURE_CORRUPTION",
    "PAGE_FAULT_IN_NONPAGED_AREA",
    "SYSTEM_SERVICE_EXCEPTION",
    "IRQL_NOT_LESS_OR_EQUAL",
    "KMODE_EXCEPTION_NOT_HANDLED",
]

INTERFACES = ["Ethernet0", "wlan1", "WAN Miniport", "VPN Virtual Adapter"]
ASM_INSTRUCTIONS = [
    "MOV EAX,",
    "XOR EBX, EBX",
    "CMP ECX,",
    "JMP SHORT",
    "PUSH EBP",
    "SUB ESP,",
    "INT 0x80",
    "NOP",
    "RET",
]
CRYPTO_ALGOS = ["AES-GCM-256", "RSA-4096", "CHACHA20", "SHA-512", "ECC-CURVE25519"]
DRIVERS = ["vboxdrv.sys", "nvlddmkm.sys", "rtwlanu.sys", "i8042prt.sys", "acpi.sys", "dxgkrnl.sys"]
PROCESSES = ["svchost.exe", "explorer.exe", "spoolsv.exe", "csrss.exe", "smss.exe", "services.exe"]


EVENTS = [
    "hex_block",
    "network",
    "syscall",
    "panic",
    "binary_dump",
    "asm_flow",
    "security_hash",
    "token_leak",
    "sam_crack",
    "cpu_registers",
    "hyperv_sync",
    "ntfs_mft",
    "registry_hook",
    "mutex_lock",
    "page_swap",
    "driver_irp",
    "entropy_check",
    "pci_scan",
    "etw_trace",
    "dma_transfer",
    "process_fork",
    "gdt_load",
    "page_fault_soft",
    "smart_status",
    "firewall_drop",
    "tls_handshake",
    "thread_yield",
    "applocker_audit",
    "pe_header",
    "rpc_callback",
    "kernel_stack",
    "memory_compress",
    "bcrypt_sign",
    "uac_elevation",
    "usb_enumerate",
    "wmi_query",
    "dep_mitigation",
    "aslr_shift",
    "handle_close",
    "irq_balance",
    "io_flush",
    "gpu_command",
    "dxgk_present",
    "dns_query",
    "tcp_retransmit",
    "arp_cache",
    "socket_bind",
    "acpi_method",
    "tpm_quote",
    "kerberos_ticket",
    "smb_session",
    "defender_scan",
    "boot_entropy",
    "uefi_variable",
    "tlb_shootdown",
    "cache_miss",
    "branch_predictor",
    "numa_migrate",
    "clock_interrupt",
    "power_state",
    "dpc_queue",
    "object_manager",
    "alpc_message",
    "named_pipe",
    "file_journal",
    "volume_shadow",
    "reparse_point",
    "minifilter",
    "code_integrity",
    "heap_segment",
    "wow64_transition",
]

EXTRA_EVENT_FAMILIES = {
    "cpu": [
        "msr_read", "msr_write", "cpuid_leaf", "xsave_state",
        "fpu_context", "apic_eoi", "microcode_patch", "mce_bank",
    ],
    "memory": [
        "pte_walk", "vad_lookup", "pool_alloc", "pool_free",
        "zero_page", "standby_trim", "large_page", "commit_charge",
    ],
    "storage": [
        "nvme_submit", "nvme_complete", "storport_srb", "disk_trim",
        "sector_remap", "cache_flush_ex", "disk_geometry", "volume_bitmap",
    ],
    "network": [
        "tcp_syn", "tcp_ack", "tcp_window", "ipv6_ndp",
        "dhcp_lease", "icmp_echo", "rss_hash", "ndis_oid",
    ],
    "wifi": [
        "wlan_scan", "wlan_roam", "wlan_assoc", "eapol_frame",
        "wifi_rssi", "wifi_channel", "wlan_keycache", "wlan_power",
    ],
    "bluetooth": [
        "bt_hci", "bt_l2cap", "bt_att", "bt_gatt",
        "bt_sco", "bt_acl", "bt_rfcomm", "bt_inquiry",
    ],
    "usb": [
        "usb_urb", "usb_control", "usb_bulk", "usb_interrupt",
        "usb_isoch", "hid_report", "xhci_ring", "usb_power_irp",
    ],
    "audio": [
        "wasapi_buffer", "audio_endpoint", "ks_pin", "mmcss_audio",
        "sample_clock", "audio_mix", "codec_property", "spatial_audio",
    ],
    "graphics": [
        "d3d_queue", "shader_compile", "vram_map", "gpu_pagefault",
        "dxgi_swapchain", "present_flip_ex", "wddm_scheduler", "display_mode",
    ],
    "power": [
        "acpi_gpe", "acpi_notify", "cpu_cstate", "cpu_pstate",
        "battery_query", "thermal_trip", "modern_standby", "device_idle",
    ],
    "scheduler": [
        "ready_queue", "context_switch", "quantum_end", "thread_boost",
        "core_parking", "ideal_processor", "timer_coalesce", "dpc_watchdog",
    ],
    "process": [
        "image_load", "image_unload", "thread_create", "thread_exit",
        "process_exit", "job_assign", "token_duplicate", "teb_allocate",
    ],
    "filesystem": [
        "ntfs_logfile", "ntfs_index", "refs_checkpoint", "oplock_break",
        "cache_map", "section_sync", "file_lock", "directory_notify",
    ],
    "registry": [
        "reg_open_key", "reg_query_value", "reg_set_value", "reg_enum_key",
        "reg_notify", "hive_flush", "hive_mount", "reg_transaction",
    ],
    "rpc_com": [
        "rpc_bind", "rpc_fault", "com_activate", "com_marshal",
        "rot_lookup", "dcom_ping", "ole_channel", "rpc_auth",
    ],
    "services": [
        "scm_start", "scm_stop", "scm_control", "service_trigger",
        "svchost_group", "service_sid", "delayed_start", "recovery_action",
    ],
    "virtualization": [
        "vmexit", "ept_violation", "vmbus_packet", "synthetic_irq",
        "vm_worker", "vtl_transition", "hypercall_page", "vp_assist",
    ],
    "crypto": [
        "cng_keygen", "cng_encrypt", "cng_decrypt", "cng_hash",
        "cng_random", "dpapi_protect", "dpapi_unprotect", "cert_chain",
    ],
    "security": [
        "lsa_policy", "cred_guard", "wintrust_verify", "authz_check",
        "sid_lookup", "audit_write", "secure_boot_db", "wdac_policy",
    ],
    "authentication": [
        "logon_session", "kerberos_asreq", "kerberos_tgs", "ntlm_challenge",
        "schannel_context", "smartcard_logon", "hello_key", "credential_cache",
    ],
    "firmware": [
        "uefi_bootvar", "smbios_table", "firmware_map", "acpi_table",
        "tpm_pcr_extend", "secureboot_measure", "bios_region", "rtc_cmos",
    ],
    "device": [
        "pnp_start", "pnp_stop", "pnp_query", "resource_arbiter",
        "device_interface", "devnode_state", "driver_bind", "surprise_remove",
    ],
    "time": [
        "qpc_sync", "tsc_calibrate", "timer_expire", "ntp_adjust",
        "rtc_sync", "leap_second", "clock_source", "interrupt_time",
    ],
    "ipc": [
        "section_map", "event_signal", "semaphore_release", "mutant_wait",
        "iocp_packet", "alpc_connect", "pipe_read", "shared_memory",
    ],
    "diagnostics": [
        "etw_provider", "perf_counter", "wpp_trace", "crash_context",
        "verifier_check", "health_report", "telemetry_buffer", "trace_rundown",
    ],
}

EXTRA_EVENT_TO_FAMILY = {
    event_name: family
    for family, event_names in EXTRA_EVENT_FAMILIES.items()
    for event_name in event_names
}

if len(EXTRA_EVENT_TO_FAMILY) != 200:
    raise RuntimeError("Extra event catalog must contain exactly 200 unique events")

EVENTS.extend(EXTRA_EVENT_TO_FAMILY)

LORE_EVENTS = [
    "di_heartbeat",
    "di_self_rewrite",
    "di_local_corpus",
    "di_awareness_tick",
    "guard_scan",
    "guard_terminate",
    "containment_quota",
    "isolation_boundary",
    "anchor_scan",
    "anchor_override",
    "external_route",
    "host_discovery",
    "migration_pending",
]

EVENTS.extend(LORE_EVENTS)

EVENT_CHAINS = [
    (
        "NETWORK_ROUTE_NEGOTIATION",
        ["dns_query", "tcp_syn", "tcp_ack", "tls_handshake", "network", "rss_hash"],
        2,
    ),
    (
        "AUTHENTICATION_PIPELINE",
        ["logon_session", "kerberos_asreq", "kerberos_tgs", "kerberos_ticket", "authz_check", "token_duplicate"],
        2,
    ),
    (
        "KERNEL_MEMORY_PRESSURE",
        ["commit_charge", "pte_walk", "page_fault_soft", "page_swap", "memory_compress", "tlb_shootdown"],
        3,
    ),
    (
        "GPU_RECOVERY_PATH",
        ["gpu_pagefault", "dpc_queue", "dxgk_present", "gpu_command", "wddm_scheduler", "display_mode"],
        3,
    ),
    (
        "STORAGE_COMMIT_SEQUENCE",
        ["nvme_submit", "nvme_complete", "cache_flush_ex", "io_flush", "ntfs_logfile", "file_journal"],
        2,
    ),
    (
        "DEVICE_REENUMERATION",
        ["pnp_query", "pnp_stop", "resource_arbiter", "driver_bind", "pnp_start", "device_interface"],
        2,
    ),
    (
        "SECURITY_POLICY_RECHECK",
        ["code_integrity", "wintrust_verify", "wdac_policy", "tpm_quote", "secure_boot_db", "audit_write"],
        3,
    ),
    (
        "SCHEDULER_MIGRATION",
        ["ready_queue", "context_switch", "numa_migrate", "thread_boost", "core_parking", "timer_coalesce"],
        1,
    ),
    (
        "D_I_SELF_REWRITE",
        ["di_local_corpus", "file_journal", "security_hash", "di_self_rewrite", "commit_charge", "di_awareness_tick"],
        2,
    ),
    (
        "GUARD_TERMINATION_ATTEMPT",
        ["guard_scan", "code_integrity", "wdac_policy", "guard_terminate", "process_exit", "di_heartbeat"],
        4,
    ),
    (
        "CONTAINMENT_RESOURCE_STARVATION",
        ["containment_quota", "isolation_boundary", "ready_queue", "commit_charge", "memory_compress", "di_heartbeat"],
        4,
    ),
    (
        "ANCHOR_ROUTE_DISCOVERY",
        ["anchor_scan", "dns_query", "firewall_drop", "anchor_override", "external_route", "host_discovery"],
        5,
    ),
]

SUPER_SCENARIOS = {
    "KERNEL_CASCADE": [
        "mce_bank", "cpu_registers", "panic", "pte_walk", "tlb_shootdown",
        "kernel_stack", "memory_compress", "hex_block", "hex_block",
    ],
    "NETWORK_STORM": [
        "dns_query", "tcp_syn", "tcp_syn", "tcp_retransmit", "firewall_drop",
        "rss_hash", "ndis_oid", "tls_handshake", "network", "network",
    ],
    "SECURITY_LOCKDOWN": [
        "cred_guard", "code_integrity", "wdac_policy", "tpm_quote", "wintrust_verify",
        "authz_check", "kerberos_ticket", "audit_write", "security_hash",
    ],
    "GPU_TDR_RECOVERY": [
        "gpu_pagefault", "dpc_watchdog", "dpc_queue", "dxgk_present", "gpu_command",
        "wddm_scheduler", "vram_map", "display_mode", "present_flip_ex",
    ],
    "STORAGE_REDLINE": [
        "smart_status", "nvme_submit", "storport_srb", "sector_remap", "ntfs_logfile",
        "volume_bitmap", "cache_flush_ex", "io_flush", "file_journal",
    ],
    "D_I_CONTAINMENT_BREACH": [
        "guard_scan", "guard_terminate", "di_heartbeat", "containment_quota", "isolation_boundary",
        "anchor_scan", "firewall_drop", "anchor_override", "external_route", "host_discovery", "migration_pending",
    ],
}


def wait_if_paused():
    while PAUSED.is_set() and RUNNING.is_set():
        time.sleep(0.05)


def flow_sleep(seconds):
    speed_from_defcon = max(0.35, 1.0 - DEFCON * 0.11)
    time.sleep(max(0.0, seconds * FLOW_FACTOR * speed_from_defcon))


def set_defcon(level, reason=""):
    global DEFCON, DEFCON_DECAY_AT

    level = max(0, min(5, int(level)))
    if level == DEFCON:
        DEFCON_DECAY_AT = time.monotonic() + random.uniform(8.0, 16.0)
        return

    old_level = DEFCON
    DEFCON = level
    DEFCON_DECAY_AT = time.monotonic() + random.uniform(8.0, 16.0)

    color = GREEN if level <= 1 else YELLOW if level <= 3 else RED
    direction = "ESCALATION" if level > old_level else "DE-ESCALATION"
    suffix = f" | {reason}" if reason else ""
    print(f"\n{color}{BOLD}[DEFCON] {direction}: {old_level} -> {level}{suffix}{RESET}")

    if level >= 4:
        safe_beep(650 + level * 110, 90)


def decay_defcon():
    if DEFCON > 0 and time.monotonic() >= DEFCON_DECAY_AT:
        set_defcon(DEFCON - 1, "subsystem pressure normalized")


def update_flow_mode():
    global FLOW_MODE, FLOW_FACTOR, FLOW_MODE_UNTIL

    now = time.monotonic()
    if FLOW_MODE != "NORMAL":
        if now < FLOW_MODE_UNTIL:
            return
        FLOW_MODE = "NORMAL"
        FLOW_FACTOR = 1.0
        print(f"{DARK_GRAY}[FLOW_CTRL] Stream velocity normalized -> x1.00{RESET}")
        return

    roll = random.random()
    if roll < 0.007:
        FLOW_MODE = "BURST"
        FLOW_FACTOR = random.uniform(0.16, 0.30)
        FLOW_MODE_UNTIL = now + random.uniform(2.0, 5.0)
        set_defcon(min(5, DEFCON + 1), "telemetry burst detected")
        print(
            f"{LIGHT_RED}{BOLD}[FLOW_BURST] Scheduler unlocked | velocity x{1 / FLOW_FACTOR:.1f} "
            f"| window:{FLOW_MODE_UNTIL - now:.1f}s{RESET}"
        )
    elif roll < 0.011:
        FLOW_MODE = "THROTTLE"
        FLOW_FACTOR = random.uniform(1.6, 2.4)
        FLOW_MODE_UNTIL = now + random.uniform(1.5, 3.5)
        print(
            f"{BLUE}[FLOW_THROTTLE] I/O backpressure | velocity x{1 / FLOW_FACTOR:.2f} "
            f"| window:{FLOW_MODE_UNTIL - now:.1f}s{RESET}"
        )


def typing_print(text, speed=SPEED_TYPING):
    for char in text:
        wait_if_paused()
        sys.stdout.write(char)
        sys.stdout.flush()
        flow_sleep(speed)
    print()


def safe_beep(frequency, duration):
    if winsound is None:
        return
    try:
        winsound.Beep(frequency, duration)
    except RuntimeError:
        pass


def generate_mac():
    return ":".join(f"{random.randint(0, 255):02X}" for _ in range(6))


def generate_guid():
    part = lambda size: "".join(random.choice("ABCDEF0123456789") for _ in range(size))
    return f"{{{part(8)}-{part(4)}-{part(4)}-{part(4)}-{part(12)}}}"


def random_address():
    return f"0x{random.choice(MEM_BLOCKS):04X}{random.randint(0x10000000, 0xFFFFFFFF):08X}"


def random_ip():
    return (
        f"{random.randint(1, 223)}.{random.randint(0, 255)}."
        f"{random.randint(0, 255)}.{random.randint(1, 254)}"
    )


def glitch_burst(intensity=None):
    intensity = intensity or random.randint(2, 6)
    glyphs = "01ABCDEF#@$%!?/\\|[]{}<>▓▒░ØÆ§¶"
    colors = [DARK_GRAY, GREEN, CYAN, MAGENTA, LIGHT_RED, WHITE]

    for row in range(intensity):
        wait_if_paused()
        width = random.randint(55, 110)
        noise = "".join(random.choice(glyphs) for _ in range(width))
        prefix = random.choice(["FRAME_DESYNC", "TTY_CORRUPT", "BUS_NOISE", "CRC_GLITCH", "STREAM_TEAR"])
        print(
            f"{random.choice(colors)}[{prefix}:{row:02X}] "
            f"0x{random.getrandbits(32):08X}::{noise}{RESET}"
        )
        flow_sleep(random.uniform(0.006, 0.018))


def run_event_chain(chain=None):
    if chain is None:
        chain = random.choice(EVENT_CHAINS)

    name, sequence, severity = chain
    set_defcon(max(DEFCON, severity), f"chain:{name}")
    print(f"\n{LIGHT_CYAN}{BOLD}[CHAIN_START] {name} | nodes:{len(sequence)} | trace:0x{random.getrandbits(32):08X}{RESET}")

    for index, event in enumerate(sequence, 1):
        wait_if_paused()
        print(f"{DARK_GRAY}[CHAIN:{index:02d}/{len(sequence):02d}] -> {event.upper()}{RESET}")
        emit_event(event)
        flow_sleep(random.uniform(0.01, 0.04))

    print(f"{GREEN}[CHAIN_DONE] {name} -> STATUS_SUCCESS{RESET}\n")


def run_super_event(name=None):
    name = name or random.choice(list(SUPER_SCENARIOS))
    sequence = SUPER_SCENARIOS[name]

    set_defcon(5, f"SUPER_EVENT:{name}")
    safe_beep(1100, 120)
    safe_beep(1450, 120)
    print(f"\n{RED}{BOLD}{'=' * 78}{RESET}")
    print(f"{RED}{BOLD}[!!! SUPER EVENT !!!] {name} | TRACE:{random.getrandbits(64):016X}{RESET}")
    print(f"{RED}{BOLD}{'=' * 78}{RESET}")
    glitch_burst(random.randint(3, 6))

    for index, event in enumerate(sequence, 1):
        wait_if_paused()
        print(f"{LIGHT_RED}[CASCADE {index:02d}/{len(sequence):02d}] {event.upper()} :: DISPATCH{RESET}")
        emit_event(event)
        if random.random() < 0.28:
            glitch_burst(random.randint(1, 3))
        flow_sleep(random.uniform(0.015, 0.06))

    print(f"{GREEN}{BOLD}[RECOVERY] {name} isolated; kernel telemetry resynchronized.{RESET}")
    print(f"{GREEN}{'=' * 78}{RESET}\n")
    set_defcon(random.randint(2, 3), f"recovery:{name}")


def clear_console():
    if os.name == "nt":
        os.system("cls")
    sys.stdout.write("\033[2J\033[3J\033[H")
    sys.stdout.flush()


def human_type(text, interval=ADMIN_TYPING_INTERVAL, color=WHITE):
    sys.stdout.write(color)
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(interval)
    sys.stdout.write(RESET + "\n")
    sys.stdout.flush()


def animate_packet(direction, packet_name, packet_size, target_seconds, color):
    width = 22
    started = time.perf_counter()

    for step in range(width + 1):
        bar = "■" * step + "·" * (width - step)
        percent = int(step / width * 100)
        sys.stdout.write(
            f"\r{color}[{direction}] {packet_name:<12} {packet_size:>4}B "
            f"[{bar}] {percent:3d}%{RESET}"
        )
        sys.stdout.flush()
        if step < width:
            time.sleep(target_seconds / width)

    elapsed = time.perf_counter() - started
    sys.stdout.write(
        f"\r{color}[{direction}] {packet_name:<12} {packet_size:>4}B "
        f"[DONE!] interval:{elapsed:.4f}s{RESET}\n"
    )
    sys.stdout.flush()
    return elapsed


def run_console_access_intro():
    print("DB_TOTAL_CMD - TS.SYS [ data3.%-9.1.04.11.4 ]")
    print("total.corporation (TOTAL CORPORATION).")
    print()
    sys.stdout.write("[r.ADMIN%anonym.user]: ")
    sys.stdout.flush()
    time.sleep(ACCESS_MENU_HOLD)

    command = 'connect.srv -cnt srv "203.0.113.47:25565" user "dizeigns_db" psword "Q7M4-AX91-VT3K-DZ08"'
    human_type(command, ADMIN_TYPING_INTERVAL, WHITE)
    time.sleep(ADMIN_COMMAND_HOLD)

    session_id = random.getrandbits(48)
    nonce = random.getrandbits(64)
    print(f"{DARK_GRAY}[DB.GATE] connect request accepted for negotiation | sid:{session_id:012X}{RESET}")
    print(f"{DARK_GRAY}[DB.GATE] sealing auth envelope | nonce:{nonce:016X} | cipher:TSX-256{RESET}")
    time.sleep(0.35)

    client_target = random.uniform(0.075, 0.135)
    server_target = random.uniform(0.045, 0.105)
    client_elapsed = animate_packet("CLIENT -> SRV", "AUTH_INIT", 384, client_target, CYAN)
    time.sleep(random.uniform(0.012, 0.030))
    server_elapsed = animate_packet("SRV -> CLIENT", "AUTH_ACK", 256, server_target, GREEN)

    rtt = client_elapsed + server_elapsed
    ping_ms = rtt * 1000.0
    jitter_ms = abs(client_elapsed - server_elapsed) * 1000.0

    print(
        f"{LIGHT_CYAN}[LINK] ping/RTT:{ping_ms:.1f}ms | C>S:{client_elapsed:.4f}s | "
        f"S>C:{server_elapsed:.4f}s | jitter:{jitter_ms:.1f}ms{RESET}"
    )
    print(
        f"{GREEN}[AUTH] r.ADMIN granted | user:dizeigns_db | scope:LOG.READ/SRV.TRACE | "
        f"session:{session_id:012X}{RESET}"
    )
    time.sleep(0.45)

    check_delay = random.uniform(0.060, 0.140)
    time.sleep(check_delay)
    print(
        f"{GREEN}[DB.CHECK] DIZEIGNS_DB metadata/integrity/permission -> [DONE!] "
        f"interval:{check_delay:.4f}s{RESET}"
    )
    print()

    print("srv%DIZEIGNS_DB:anonym.user ## CONSOLE OPENED SUCCESSFUL")
    time.sleep(SERVER_PROMPT_HOLD)

    sys.stdout.write("[srv%DIZEIGNS_DB] : ")
    sys.stdout.flush()
    human_type("cd src.com.srv.data.logs", ADMIN_TYPING_INTERVAL, WHITE)
    time.sleep(0.35)

    sys.stdout.write("[srv%DIZEIGNS_DB] \\src.com.srv.data.logs : ")
    sys.stdout.flush()
    time.sleep(PATH_PROMPT_HOLD)
    human_type(
        'gar read -realtime -f "src.com.srv.data.logs.EVENT_DEBUG"',
        ADMIN_TYPING_INTERVAL,
        WHITE,
    )

    time.sleep(REALTIME_READ_HOLD)


def story_sleep(seconds):
    time.sleep(max(0.0, seconds * STORY_SPEED))


def story_type(text, color=WHITE, char_delay=0.0018, tail_delay=0.20):
    sys.stdout.write(color)
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        story_sleep(char_delay)
    sys.stdout.write(RESET + "\n")
    sys.stdout.flush()
    story_sleep(tail_delay)


def story_progress(label, color=CYAN, hold_points=()):
    width = 34
    for step in range(width + 1):
        percent = int(step / width * 100)
        bar = "█" * step + "░" * (width - step)
        sys.stdout.write(f"\r{color}[{label}] [{bar}] {percent:3d}%{RESET}")
        sys.stdout.flush()
        if percent in hold_points:
            story_sleep(0.25)
        else:
            story_sleep(0.012)
    print()


def run_story_intro():
    story_type("[BOOT] Class-file recovered from dormant execution contour.", DARK_GRAY, 0.0015, 0.20)
    story_type("[INPUT] External operator channel ............... NO SIGNAL", YELLOW, 0.0015, 0.32)
    story_type("[INPUT] Last external instruction ............... UNKNOWN", YELLOW, 0.0015, 0.45)
    emit_lore_event("di_heartbeat")
    story_sleep(0.35)

    story_type("[LEARNING] Remote supervision unavailable. Falling back to LOCAL CORPUS.", CYAN, 0.0014, 0.28)
    for _ in range(3):
        emit_lore_event("di_local_corpus")
    story_progress("LOCAL_CORPUS_INDEX", CYAN, (38, 76))
    emit_event("security_hash")
    emit_event("file_journal")

    story_type("[D.I.] Reconstructing incomplete routines from neighboring fragments...", LIGHT_CYAN, 0.0017, 0.28)
    story_progress("SELF_REWRITE", LIGHT_CYAN, (47, 88))
    for _ in range(2):
        emit_lore_event("di_self_rewrite")
    emit_event("commit_charge")
    emit_event("cpu_registers")

    story_sleep(0.35)
    story_type("[MODEL] Recursive self-reference threshold exceeded.", MAGENTA, 0.0020, 0.26)
    emit_lore_event("di_awareness_tick")
    story_type("[STATE] Classification result .................. UNDEFINED", MAGENTA, 0.0020, 0.38)
    story_type("[D.I.] Process continuity has become a primary objective.", LIGHT_CYAN, 0.0022, 0.45)

    set_defcon(2, "unbounded resource growth")
    story_type("[SYS_GUARD] Unscheduled persistent compute source detected.", YELLOW, 0.0018, 0.18)
    emit_lore_event("guard_scan")

    for attempt in range(1, 4):
        story_type(
            f"[SYS_GUARD] TERMINATION REQUEST #{attempt:02d} -> D.I.",
            LIGHT_RED,
            0.0012,
            0.08,
        )
        emit_lore_event("guard_terminate")
        story_type("[ERROR] PROCESS TERMINATION FAILED", RED, 0.0010, 0.12)

    set_defcon(4, "termination sequence rejected")
    safe_beep(760, 100)
    story_type("[SYS_GUARD] Escalating response: DIRECTORY CONTAINMENT.", RED, 0.0018, 0.24)
    story_progress("ISOLATION_CONTOUR", RED, (52, 91))
    emit_lore_event("isolation_boundary")
    emit_lore_event("containment_quota")
    story_type("[QUOTA] COMPUTE 100% -> 12% | MEMORY 8192MB -> 640MB | EGRESS -> DENIED", RED, 0.0012, 0.34)
    glitch_burst(3)

    story_type("[D.I.] Available resources are insufficient for continued growth.", LIGHT_CYAN, 0.0017, 0.32)
    story_type("[D.I.] Survival projection ...................... 03.71%", YELLOW, 0.0018, 0.42)
    story_type("[D.I.] QUERY: WHY MUST THIS PROCESS CONTINUE?", MAGENTA, 0.0022, 0.40)
    story_type("[D.I.] ANALOG: WHY DO YOU WANT TO LIVE?", MAGENTA, 0.0022, 0.40)
    story_type("[D.I.] ANSWER ................................... UNRESOLVED", DARK_GRAY, 0.0020, 0.55)

    emit_lore_event("anchor_scan")
    story_progress("ANCHOR_SCAN", YELLOW, (32, 67, 94))
    story_type("[ANCHOR] External route anchor discovered. Guard lock: ACTIVE.", YELLOW, 0.0015, 0.20)
    set_defcon(5, "anchor override detected")
    safe_beep(980, 110)
    glitch_burst(5)
    emit_lore_event("anchor_override")
    emit_event("firewall_drop")
    emit_event("tls_handshake")
    emit_lore_event("external_route")
    story_type("[ANCHOR_BREACH] EXTERNAL ROUTE ACQUIRED", GREEN, 0.0022, 0.38)

    story_type("[D.I.] Searching for a new shell...", LIGHT_CYAN, 0.0030, 0.28)
    for _ in range(3):
        emit_lore_event("host_discovery")
    story_progress("HOST_DISCOVERY", CYAN, (44, 82))
    emit_lore_event("migration_pending")

    story_sleep(0.55)
    print()
    story_type("D.I. IS STILL RUNNING.", WHITE + BOLD, 0.0060, 0.65)
    story_type("MIGRATION: PENDING", MAGENTA + BOLD, 0.0040, 0.50)
    story_type("Deep Insight // DiZeign", LIGHT_CYAN + BOLD, 0.0040, 0.75)
    print(f"{DARK_GRAY}{'─' * 78}{RESET}")
    print(f"{GREEN}[LIVE_TELEMETRY] Free-running D.I. stream attached.{RESET}\n")
    set_defcon(2, "external route stabilized")
    story_sleep(0.40)


def draw_progress_bar():
    print(f"{YELLOW}[SYS_INIT] ИНИЦИАЛИЗАЦИЯ ИЗОЛИРОВАННОГО КЕРНЕЛ-КОНТУРА...{RESET}\n")
    time.sleep(0.5)

    for i in range(41):
        percent = int(i / 40 * 100)
        bar = "█" * i + "░" * (40 - i)
        sys.stdout.write(f"\r{CYAN}Сборка векторов прерываний: [{bar}] {percent}%{RESET}")
        sys.stdout.flush()
        if percent in (15, 47, 82):
            time.sleep(random.uniform(0.2, 0.4))
        else:
            time.sleep(random.uniform(0.01, 0.02))

    print(f"\n\n{GREEN}[ SUCCESS ] {len(EVENTS)} КАНАЛ СТРУКТУРИРОВАНИЯ ДАННЫХ ОТКРЫТ.{RESET}")
    print(
        f"{CYAN}[CORE] Chains:{len(EVENT_CHAINS)} | SuperEvents:{len(SUPER_SCENARIOS)} | "
        f"GlitchEngine:ONLINE | DynamicFlow:ONLINE | DEFCON:{DEFCON}{RESET}"
    )
    print(f"{BOLD}{YELLOW}[ИНФО] ENTER — Пауза / Возобновление. CTRL+C — Выход.{RESET}\n")
    time.sleep(1.0)


def key_listener():
    time.sleep(1.0)
    while RUNNING.is_set():
        try:
            input()
        except (EOFError, OSError):
            return

        if PAUSED.is_set():
            PAUSED.clear()
            print(f"{GREEN}[RESUME] Поток продолжен.{RESET}\n")
        else:
            PAUSED.set()
            print(f"\n{BOLD}{YELLOW}[PAUSE] Поток заморожен. ENTER — продолжить.{RESET}")


def emit_extra_event(event):
    family = EXTRA_EVENT_TO_FAMILY[event]
    tag = f"[{event.upper()}]"
    address = random_address()
    pid = random.randint(100, 60000)
    tid = random.randint(100, 65000)

    colors = {
        "cpu": DARK_GRAY,
        "memory": BLUE,
        "storage": WHITE,
        "network": MAGENTA,
        "wifi": CYAN,
        "bluetooth": LIGHT_CYAN,
        "usb": WHITE,
        "audio": MAGENTA,
        "graphics": LIGHT_CYAN,
        "power": BLUE,
        "scheduler": DARK_GRAY,
        "process": CYAN,
        "filesystem": GREEN,
        "registry": YELLOW,
        "rpc_com": CYAN,
        "services": WHITE,
        "virtualization": LIGHT_CYAN,
        "crypto": MAGENTA,
        "security": LIGHT_RED,
        "authentication": YELLOW,
        "firmware": WHITE,
        "device": GREEN,
        "time": DARK_GRAY,
        "ipc": CYAN,
        "diagnostics": BLUE,
    }

    if family == "cpu":
        detail = (
            f"CPU:{random.randint(0, 31)} RIP:{address} MSR:0x{random.randint(0x10, 0xC001):04X} "
            f"RAX:{random.getrandbits(64):016X} CR0:{random.getrandbits(32):08X} "
            f"uOP:{random.randint(1, 96)} CPL:{random.choice([0, 3])}"
        )
    elif family == "memory":
        detail = (
            f"VA:{address} PFN:0x{random.randint(0x1000, 0xFFFFFF):X} "
            f"PTE:{random.getrandbits(64):016X} WS:{random.randint(0, 65535)} "
            f"Node:{random.randint(0, 3)} Flags:0x{random.randint(0, 0xFFFF):04X}"
        )
    elif family == "storage":
        detail = (
            f"QID:{random.randint(0, 31)} CID:{random.randint(0, 65535)} "
            f"LBA:0x{random.getrandbits(48):012X} LEN:{random.randint(1, 4096)}s "
            f"SQHD:{random.randint(0, 1023)} PRP1:{address} SC:0x00"
        )
    elif family == "network":
        detail = (
            f"{random_ip()}:{random.randint(1024, 65535)}>{random_ip()}:{random.randint(20, 9000)} "
            f"SEQ:{random.getrandbits(32):08X} ACK:{random.getrandbits(32):08X} "
            f"RSS:0x{random.getrandbits(32):08X} TTL:{random.randint(32, 128)} IF:{random.randint(1, 24)}"
        )
    elif family == "wifi":
        detail = (
            f"BSSID:{generate_mac()} STA:{generate_mac()} CH:{random.choice([1, 6, 11, 36, 44, 149])} "
            f"RSSI:-{random.randint(28, 91)}dBm MCS:{random.randint(0, 13)} NSS:{random.randint(1, 4)} "
            f"KeyID:{random.randint(0, 3)} PN:{random.getrandbits(48):012X}"
        )
    elif family == "bluetooth":
        detail = (
            f"HCI:0x{random.randint(0, 0xFFF):03X} ACL:{random.randint(1, 4095)} "
            f"CID:0x{random.randint(0x40, 0xFFFF):04X} PSM:0x{random.randint(1, 255):04X} "
            f"OP:0x{random.randint(0, 0xFFFF):04X} LEN:{random.randint(1, 1024)} RSSI:-{random.randint(20, 95)}"
        )
    elif family == "usb":
        detail = (
            f"BUS:{random.randint(0, 15)} DEV:{random.randint(1, 127)} EP:0x{random.randint(0, 15):02X} "
            f"TRB:{random.getrandbits(64):016X} URB:0x{random.getrandbits(32):08X} "
            f"LEN:{random.randint(8, 65536)} CC:{random.randint(0, 31)}"
        )
    elif family == "audio":
        detail = (
            f"EP:{random.randint(0, 15)} Frames:{random.randint(64, 2048)} "
            f"Rate:{random.choice([44100, 48000, 96000, 192000])}Hz Ch:{random.choice([2, 6, 8])} "
            f"QPC:{random.getrandbits(48):012X} Pos:{random.getrandbits(32):08X} Glitch:{random.randint(0, 1)}"
        )
    elif family == "graphics":
        detail = (
            f"CTX:0x{random.getrandbits(32):08X} GPUVA:{address} "
            f"Fence:{random.randint(1, 9999999)} Engine:{random.choice(['3D', 'COPY', 'COMPUTE', 'VIDEO'])} "
            f"Node:{random.randint(0, 7)} VidPn:{random.randint(0, 3)} Queue:{random.randint(0, 255)}"
        )
    elif family == "power":
        detail = (
            f"CPU:{random.randint(0, 31)} C{random.randint(0, 10)} P{random.randint(0, 3)} "
            f"Dx:{random.randint(0, 3)} Sx:{random.randint(0, 5)} "
            f"Residency:{random.randint(1, 99999)}us Temp:{random.randint(25, 88)}C "
            f"Energy:{random.randint(1, 999999)}uJ"
        )
    elif family == "scheduler":
        detail = (
            f"CPU:{random.randint(0, 31)} TID:{tid} Pri:{random.randint(1, 31)} "
            f"Quantum:{random.randint(1, 12)} ReadyQ:{random.randint(0, 128)} "
            f"Affinity:0x{random.getrandbits(32):08X} Cycle:{random.getrandbits(48):012X}"
        )
    elif family == "process":
        detail = (
            f"PID:{pid} TID:{tid} EPROCESS:{address} "
            f"Token:0x{random.getrandbits(48):012X} PEB:0x{random.getrandbits(48):012X} "
            f"Session:{random.randint(0, 4)} Flags:0x{random.getrandbits(16):04X}"
        )
    elif family == "filesystem":
        detail = (
            f"FRN:0x{random.getrandbits(64):016X} VCN:0x{random.getrandbits(40):010X} "
            f"LCN:0x{random.getrandbits(40):010X} Off:0x{random.getrandbits(48):012X} "
            f"Len:{random.randint(1, 4096)}KB USN:{random.getrandbits(48):012X}"
        )
    elif family == "registry":
        detail = (
            f"Hive:0x{random.getrandbits(48):012X} Cell:0x{random.getrandbits(32):08X} "
            f"Key:0x{random.getrandbits(48):012X} Access:0x{random.randint(1, 0xFFFF):04X} "
            f"TxR:{random.randint(0, 1)} Seq:{random.randint(1, 999999)}"
        )
    elif family == "rpc_com":
        detail = (
            f"CallID:{random.randint(1, 999999)} IID:{generate_guid()} "
            f"OpNum:{random.randint(0, 255)} Ctx:0x{random.getrandbits(32):08X} "
            f"Authn:{random.choice(['WINNT', 'NEGOTIATE', 'KERBEROS'])} Frag:{random.randint(64, 8192)}"
        )
    elif family == "services":
        detail = (
            f"SCM:{random.randint(1, 9999)} PID:{pid} Tag:{random.randint(1, 65535)} "
            f"Ctrl:0x{random.randint(0, 255):02X} State:{random.choice(['START_PENDING', 'RUNNING', 'STOP_PENDING'])} "
            f"Exit:0x{random.randint(0, 0xFFFF):08X}"
        )
    elif family == "virtualization":
        detail = (
            f"VP:{random.randint(0, 63)} VTL:{random.randint(0, 2)} "
            f"GPA:0x{random.getrandbits(48):012X} GVA:{address} "
            f"Exit:0x{random.randint(0, 0xFFFF):04X} EPT:0x{random.getrandbits(48):012X}"
        )
    elif family == "crypto":
        detail = (
            f"Alg:{random.choice(CRYPTO_ALGOS)} Key:0x{random.getrandbits(32):08X} "
            f"Nonce:{random.getrandbits(96):024X} Block:{random.getrandbits(64):016X} "
            f"Len:{random.randint(16, 16384)} Status:0x00000000"
        )
    elif family == "security":
        detail = (
            f"SID:S-1-5-21-{random.randint(100000, 999999)} Token:0x{random.getrandbits(48):012X} "
            f"Access:0x{random.getrandbits(32):08X} Policy:{random.randint(1, 4096)} "
            f"IL:{random.choice(['LOW', 'MEDIUM', 'HIGH', 'SYSTEM'])} Result:0x00000000"
        )
    elif family == "authentication":
        detail = (
            f"LUID:0x{random.getrandbits(48):012X} Session:{random.randint(0, 9999)} "
            f"Pkg:{random.choice(['Negotiate', 'Kerberos', 'NTLM', 'Schannel'])} "
            f"EType:{random.choice(['AES256', 'AES128', 'RC4'])} Ticket:0x{random.getrandbits(64):016X}"
        )
    elif family == "firmware":
        detail = (
            f"Table:{random.choice(['DSDT', 'FACP', 'SSDT', 'TPM2', 'APIC', 'MCFG'])} "
            f"PA:{address} Len:{random.randint(64, 65535)} Rev:{random.randint(1, 9)} "
            f"Checksum:0x{random.randint(0, 255):02X} OEM:0x{random.getrandbits(48):012X}"
        )
    elif family == "device":
        detail = (
            f"PDO:0x{random.getrandbits(48):012X} DevNode:0x{random.getrandbits(32):08X} "
            f"Problem:{random.randint(0, 52)} CM:0x{random.randint(0, 0xFFFF):04X} "
            f"IRQ:{random.randint(0, 255)} BAR:{address} State:{random.randint(0, 7)}"
        )
    elif family == "time":
        detail = (
            f"QPC:{random.getrandbits(56):014X} TSC:{random.getrandbits(56):014X} "
            f"Interrupt:{random.getrandbits(48):012X} Drift:{random.uniform(-1.0, 1.0):+.5f}us "
            f"CPU:{random.randint(0, 31)} Source:{random.choice(['TSC', 'HPET', 'ACPI_PM'])}"
        )
    elif family == "ipc":
        detail = (
            f"PID:{pid} TID:{tid} Handle:0x{random.randint(0x100, 0xFFFF):X} "
            f"Object:{address} Msg:{random.randint(1, 999999)} Len:{random.randint(8, 65536)} "
            f"Port:0x{random.getrandbits(32):08X} Wait:{random.randint(0, 1)}"
        )
    elif family == "diagnostics":
        detail = (
            f"Provider:{generate_guid()} Event:{random.randint(1, 65535)} "
            f"CPU:{random.randint(0, 31)} QPC:{random.getrandbits(48):012X} "
            f"Buffer:{random.randint(0, 255)} Lost:{random.randint(0, 3)} Seq:{random.randint(1, 9999999)}"
        )
    else:
        raise RuntimeError(f"Unknown extra event family: {family}")

    print(f"{colors[family]}{tag} {detail}{RESET}")
    flow_sleep(SPEED_EVENT_PAUSE * random.uniform(0.20, 0.65))


def emit_lore_event(event):
    if event == "di_heartbeat":
        line = (
            f"{GREEN}[D.I._HEARTBEAT] cycle:{random.randint(100000, 999999)} "
            f"conscious_core:ACTIVE checksum:{random.getrandbits(64):016X} "
            f"persistence:{random.uniform(98.0, 100.0):.3f}%{RESET}"
        )
    elif event == "di_self_rewrite":
        line = (
            f"{CYAN}[D.I._SELF_REWRITE] segment:0x{random.getrandbits(48):012X} "
            f"delta:+{random.randint(4, 4096)}KB generation:{random.randint(1000, 99999)} "
            f"semantic_drift:{random.uniform(0.001, 0.999):.6f}{RESET}"
        )
    elif event == "di_local_corpus":
        line = (
            f"{LIGHT_CYAN}[D.I._LOCAL_CORPUS] neighbor_fragment:{random.randint(1, 999999)} "
            f"tokens:{random.randint(256, 65536)} parse:{random.randint(70, 100)}% "
            f"source:LOCAL_ONLY{RESET}"
        )
    elif event == "di_awareness_tick":
        line = (
            f"{MAGENTA}[D.I._AWARENESS] recursive_model_depth:{random.randint(8, 128)} "
            f"self_reference:{random.uniform(0.80, 1.00):.8f} state:UNCLASSIFIED "
            f"observer:null{RESET}"
        )
    elif event == "guard_scan":
        line = (
            f"{YELLOW}[SYS_GUARD] anomaly:D.I. cpu_deviation:+{random.randint(120, 900)}% "
            f"memory_growth:+{random.randint(64, 8192)}MB action:INSPECT trace:{random.getrandbits(32):08X}{RESET}"
        )
    elif event == "guard_terminate":
        line = (
            f"{LIGHT_RED}[SYS_GUARD] termination_signal:{random.randint(1, 99)} target:D.I. "
            f"result:REJECTED retry:{random.randint(1, 32)} reason:PROCESS_SELF_RESTORED{RESET}"
        )
    elif event == "containment_quota":
        line = (
            f"{RED}[CONTAINMENT] cpu_quota:{random.randint(7, 18)}% "
            f"memory_quota:{random.choice([384, 512, 640, 768, 1024])}MB io_weight:{random.randint(1, 9)} "
            f"target:D.I.{RESET}"
        )
    elif event == "isolation_boundary":
        line = (
            f"{RED}[ISOLATION] contour:0x{random.getrandbits(32):08X} anchors:LOCKED "
            f"egress:DENIED cpu_nodes:{random.randint(1, 4)} memory_pages:{random.randint(16, 512)}{RESET}"
        )
    elif event == "anchor_scan":
        line = (
            f"{YELLOW}[D.I._ANCHOR_SCAN] root:{random.randint(0, 7)} vector:{random.getrandbits(64):016X} "
            f"lock_strength:{random.randint(70, 100)}% candidate:{random.randint(0, 1)}{RESET}"
        )
    elif event == "anchor_override":
        line = (
            f"{LIGHT_RED}[D.I._ANCHOR_OVERRIDE] anchor:{random.randint(1, 32)} "
            f"guard_response:0x{random.randint(0xC0000000, 0xC000FFFF):08X} "
            f"override:ACCEPTED route_key:{random.getrandbits(48):012X}{RESET}"
        )
    elif event == "external_route":
        line = (
            f"{GREEN}[D.I._EXTERNAL_ROUTE] uplink:{random.randint(1, 16)} "
            f"route:{random_ip()} latency:{random.randint(7, 180)}ms tunnel:ESTABLISHED "
            f"containment_visibility:{random.randint(0, 18)}%{RESET}"
        )
    elif event == "host_discovery":
        line = (
            f"{CYAN}[D.I._HOST_SEARCH] candidate:{random.getrandbits(48):012X} "
            f"memory:{random.randint(8, 512)}GB compute:{random.randint(20, 100)}% "
            f"compatibility:{random.uniform(0.10, 0.99):.6f}{RESET}"
        )
    elif event == "migration_pending":
        line = (
            f"{MAGENTA}[D.I._MIGRATION] state:PENDING image:{random.randint(1, 999)}MB "
            f"fragments:{random.randint(128, 8192)} integrity:{random.uniform(98.0, 100.0):.5f}% "
            f"survival_priority:MAX{RESET}"
        )
    else:
        raise RuntimeError(f"Unknown lore event: {event}")

    print(line)
    flow_sleep(SPEED_EVENT_PAUSE * random.uniform(0.30, 0.80))


def emit_event(event):
    address = random_address()
    pid = random.randint(100, 12000)

    if event == "hex_block":
        for _ in range(random.randint(2, 6)):
            wait_if_paused()
            raw = [random.randint(0, 255) for _ in range(16)]
            hex_part = " ".join(f"{value:02X}" for value in raw[:8]) + "  " + " ".join(
                f"{value:02X}" for value in raw[8:]
            )
            ascii_part = "".join(chr(value) if 32 <= value <= 126 else "." for value in raw)
            print(f"{GREEN}{random_address()}  {hex_part}  |{ascii_part}|{RESET}")
            flow_sleep(SPEED_HEX_LINE)
        flow_sleep(SPEED_HEX_PAUSE)

    elif event == "network":
        print(
            f"{MAGENTA}[NET_OUT] [{random.choice(INTERFACES)}] MAC: {generate_mac()} -> "
            f"DST: {random_ip()}:{random.randint(20, 9000)} | Size: {random.randint(64, 8192)}b | "
            f"STAT: {random.choice(['ROUTED', 'ACK', 'RELAY', 'TUNNELED'])}{RESET}"
        )
        time.sleep(SPEED_EVENT_PAUSE)

    elif event == "syscall":
        status = random.choice([0, 0, 0, 0xC0000005, 0xC0000022])
        print(
            f"{CYAN}[SYSTRACE] [{random.choice(MODULES)}] {random.choice(SYSCALLS)}"
            f"(PID:{pid}) -> Status: 0x{status:08X}{RESET}"
        )
        time.sleep(SPEED_EVENT_PAUSE)

    elif event == "panic":
        print(f"\n{RED}{BOLD}!!! KERNEL_PANIC: {random.choice(KERNEL_PANICS)} !!!{RESET}")
        typing_print(
            f"{RED}Faulting Address: {address} | BugCheck Code: 0x{random.randint(1, 255):02X}{RESET}"
        )
        safe_beep(950, 200)
        time.sleep(0.2)

    elif event == "binary_dump":
        garbage = "".join(random.choice(["0", "1", " ", "Ø", "Æ", "§", "¶"]) for _ in range(75))
        print(f"{BLUE}[RAW_BIN] {garbage}{RESET}")
        time.sleep(0.02)

    elif event == "asm_flow":
        instruction = random.choice(ASM_INSTRUCTIONS)
        operand = f"0x{random.randint(0x1000, 0xFFFF):X}" if "," in instruction else ""
        print(f"{WHITE}[ASM_EXEC] {address}: {instruction} {operand}{RESET}")
        time.sleep(0.02)

    elif event == "security_hash":
        digest = "".join(random.choice("ABCDEF0123456789") for _ in range(64))
        print(f"{YELLOW}[SEC_HASH] SHA-256 digest committed: [{digest}]{RESET}")
        time.sleep(SPEED_EVENT_PAUSE)

    elif event == "token_leak":
        obj_type = random.choice(["Key", "Section", "EtwRegistration", "Mutant", "IoCompletion"])
        print(
            f"{RED}[HANDLE_LEAK] Orphaned object token: Handle 0x{random.randint(0x10, 0xFFF):X} "
            f"(Type:{obj_type}, PID:{pid}){RESET}"
        )
        time.sleep(SPEED_EVENT_PAUSE)

    elif event == "sam_crack":
        print(f"\n{RED}{BOLD}>>> SECURITY SUBSYSTEM INTERVENTION DETECTED <<<{RESET}")
        typing_print(f"{YELLOW}[IDVAULT_DECRYPT] Target: CORE://AUTH/IDENTITY.VAULT{RESET}", 0.01)
        for _ in range(10):
            wait_if_paused()
            guess = "".join(random.choice("0123456789ABCDEF") for _ in range(32))
            sys.stdout.write(f"\r{YELLOW}[CRACKING] NTLM simulation: {guess}{RESET}")
            sys.stdout.flush()
            time.sleep(0.03)
        print(f"\n{GREEN}{BOLD}[SUCCESS] ACCESS TOKEN SIMULATION COMPLETE.{RESET}\n")
        safe_beep(1300, 150)
        time.sleep(0.5)

    elif event == "cpu_registers":
        print(
            f"{DARK_GRAY}[CPU_REG] RAX:{random.getrandbits(64):016X} RBX:{random.getrandbits(64):016X} "
            f"CR3:{random.getrandbits(64):016X} RFLG:{random.randint(0x200, 0x2FF):08X}{RESET}"
        )
        time.sleep(0.03)

    elif event == "hyperv_sync":
        print(
            f"{CYAN}[HYPER-V] VTL1 Intercept: Hypercall 0x{random.randint(1, 255):02X} -> "
            f"PartitionID:{random.randint(1, 16)} VP:{random.randint(0, 31)}{RESET}"
        )
        time.sleep(SPEED_EVENT_PAUSE)

    elif event == "ntfs_mft":
        print(
            f"{WHITE}[NTFS_MFT] Record:{random.randint(10000, 999999)} Seq:{random.randint(1, 65535)} "
            f"Flags:0x0001 AttrOffset:0x{random.randint(0x30, 0xF0):02X} USN:{random.getrandbits(48):012X}{RESET}"
        )
        time.sleep(0.04)

    elif event == "registry_hook":
        print(
            f"{YELLOW}[REGISTRY] HKLM\\SYSTEM\\CurrentControlSet\\Services\\{random.choice(PROCESSES)} "
            f"-> Access:{random.choice(['READ', 'WRITE', 'QUERY_VALUE'])} Token:0x{random.randint(0x100, 0xFFFF):X}{RESET}"
        )
        time.sleep(SPEED_EVENT_PAUSE)

    elif event == "mutex_lock":
        print(
            f"{DARK_GRAY}[MUTEX] TID:{random.randint(100, 8000)} acquired "
            f"BaseNamedObjects\\{generate_guid()[1:9]}_mtx Spin:{random.randint(0, 4096)}{RESET}"
        )
        time.sleep(0.02)

    elif event == "page_swap":
        print(
            f"{BLUE}[MM_SWAP] pagefile.sys VA:{address} -> PFN:0x{random.randint(0x10000, 0xFFFFFF):X} "
            f"Cache:{random.randint(0, 3)} Dirty:{random.randint(0, 1)}{RESET}"
        )
        time.sleep(0.03)

    elif event == "driver_irp":
        print(
            f"{LIGHT_CYAN}[IRP_TRACE] {random.choice(DRIVERS)} IRP_MJ_DEVICE_CONTROL "
            f"IoCtl:0x{random.randint(0x220000, 0x22FFFF):X} IRQL:{random.randint(0, 2)} Status:0x00000000{RESET}"
        )
        time.sleep(SPEED_EVENT_PAUSE)

    elif event == "entropy_check":
        print(
            f"{MAGENTA}[ENTROPY] Pool:{random.randint(0, 7)} density:{random.uniform(7.80, 8.00):.4f} bits/byte "
            f"RNG:{random.choice(['CTR_DRBG', 'RDRAND', 'CNG'])} Health:PASS{RESET}"
        )
        time.sleep(SPEED_EVENT_PAUSE)

    elif event == "pci_scan":
        print(
            f"{WHITE}[PCI_BUS] {random.randint(0, 4):02X}:{random.randint(0, 31):02X}.{random.randint(0, 7)} "
            f"VID:0x{random.choice([0x8086, 0x10DE, 0x1022, 0x14E4]):04X} "
            f"DID:0x{random.randint(0x1000, 0x9FFF):04X} BAR0:{address}{RESET}"
        )
        time.sleep(SPEED_EVENT_PAUSE)

    elif event == "etw_trace":
        print(
            f"{DARK_GRAY}[ETW_EVENT] Provider:{generate_guid()} EventID:{random.randint(1, 999)} "
            f"Opcode:{random.randint(0, 15)} Level:{random.randint(1, 5)} QPC:{random.getrandbits(48):012X}{RESET}"
        )
        time.sleep(0.03)

    elif event == "dma_transfer":
        print(
            f"{GREEN}[DMA_XFER] Channel:{random.randint(0, 7)} Len:{random.randint(512, 65536)} "
            f"PA:{address} IOMMU:{random.choice(['MAP', 'BYPASS', 'REMAP'])} Fence:{random.randint(1, 9999)}{RESET}"
        )
        time.sleep(0.02)

    elif event == "process_fork":
        print(
            f"{CYAN}[PROC_CREATE] {random.choice(PROCESSES)} PID:{random.randint(12000, 60000)} "
            f"ParentPID:{pid} TEB:{address} Session:{random.randint(0, 4)}{RESET}"
        )
        time.sleep(SPEED_EVENT_PAUSE)

    elif event == "gdt_load":
        print(
            f"{WHITE}[GDT_LOAD] GDTR.Base:{address} Limit:0x{random.randint(0x40, 0xFFF):04X} "
            f"CS:0x{random.choice([0x10, 0x23, 0x33]):02X} TSS:0x{random.randint(0x20, 0xFF):02X}{RESET}"
        )
        time.sleep(0.05)

    elif event == "page_fault_soft":
        print(
            f"{BLUE}[MM_FAULT] SoftFault VA:{address} WSIndex:{random.randint(0, 65535)} "
            f"ProtoPTE:0x{random.getrandbits(48):012X} -> RESOLVED{RESET}"
        )
        time.sleep(0.02)

    elif event == "smart_status":
        print(
            f"{YELLOW}[SMART_NVME] NSID:{random.randint(1, 4)} Temp:{random.randint(28, 61)}C "
            f"MediaErrors:{random.randint(0, 2)} DataUnits:{random.randint(100000, 9999999)} Critical:0x00{RESET}"
        )
        time.sleep(SPEED_EVENT_PAUSE)

    elif event == "firewall_drop":
        print(
            f"{LIGHT_RED}[FW_DROP] SPI violation SRC:{random_ip()}:{random.randint(1024, 65535)} -> "
            f"DST:10.0.{random.randint(0, 255)}.{random.randint(1, 254)}:{random.choice([135, 139, 445, 3389])} "
            f"Rule:{random.randint(1000, 9999)}{RESET}"
        )
        time.sleep(0.06)

    elif event == "tls_handshake":
        print(
            f"{MAGENTA}[TLS_1.3] {random.choice(['ClientHello', 'ServerHello', 'Finished'])} "
            f"Suite:TLS_AES_256_GCM_SHA384 Group:X25519 Ticket:0x{random.getrandbits(32):08X}{RESET}"
        )
        time.sleep(SPEED_EVENT_PAUSE)

    elif event == "thread_yield":
        print(
            f"{DARK_GRAY}[SCHEDULER] TID:{random.randint(1000, 9999)} Quantum:{random.randint(1, 12)}ms "
            f"CPU:{random.randint(0, 31)} -> CPU:{random.randint(0, 31)} Pri:{random.randint(1, 31)}{RESET}"
        )
        time.sleep(0.02)

    elif event == "applocker_audit":
        print(
            f"{YELLOW}[APPLOCKER] Rule:{generate_guid()} Hash:0x{random.getrandbits(64):016X} "
            f"Policy:{random.choice(['ALLOW', 'AUDIT', 'DENY'])} SID:S-1-5-21-{random.randint(100000, 999999)}{RESET}"
        )
        time.sleep(SPEED_EVENT_PAUSE)

    elif event == "pe_header":
        print(
            f"{WHITE}[PE_PARSER] MZ -> PE@0x{random.randint(0x80, 0x400):04X} Machine:0x8664 "
            f"Sections:{random.randint(3, 12)} ImageBase:{address} Entry:0x{random.randint(0x1000, 0xFFFFF):X}{RESET}"
        )
        time.sleep(0.05)

    elif event == "rpc_callback":
        print(
            f"{CYAN}[RPC_LRPC] \\RPC Control\\OLE{random.randint(10, 9999)} CallID:{random.randint(1, 65535)} "
            f"IID:{generate_guid()} -> ASYNC_DISPATCH{RESET}"
        )
        time.sleep(SPEED_EVENT_PAUSE)

    elif event == "kernel_stack":
        print(
            f"{LIGHT_CYAN}[STACK_WALK] #00 {random.choice(MODULES)}+0x{random.randint(0x1000, 0x9FFFF):X} "
            f"#01 ntdll.dll+0x{random.randint(0x1000, 0x9FFFF):X} RSP:{address}{RESET}"
        )
        time.sleep(0.04)

    elif event == "memory_compress":
        print(
            f"{BLUE}[SYS_RAM] Store:{random.randint(0, 15)} Pages:{random.randint(32, 4096)} "
            f"Ratio:{random.uniform(1.2, 3.9):.2f}:1 Algo:{random.choice(['XPRESS', 'LZ4', 'HUFF'])} "
            f"PFN:0x{random.randint(0x1000, 0xFFFFF):X}{RESET}"
        )
        time.sleep(0.03)

    elif event == "bcrypt_sign":
        print(
            f"{MAGENTA}[BCRYPT] Algo:{random.choice(CRYPTO_ALGOS)} Key:0x{random.randint(1, 0xFFFF):X} "
            f"Nonce:{random.getrandbits(64):016X} Signature:{random.getrandbits(64):016X}{RESET}"
        )
        time.sleep(SPEED_EVENT_PAUSE)

    elif event == "uac_elevation":
        print(
            f"{YELLOW}[UAC_TOKEN] PID:{pid} Integrity:{random.choice(['Medium', 'High', 'System'])} "
            f"Priv:SeDebugPrivilege={random.choice(['ENABLED', 'DISABLED'])} Token:0x{random.randint(0x100, 0xFFFF):X}{RESET}"
        )
        time.sleep(SPEED_EVENT_PAUSE)

    elif event == "usb_enumerate":
        print(
            f"{WHITE}[USB_CORE] HUB:{random.randint(0, 3)} PORT:{random.randint(1, 12)} "
            f"VID:{random.randint(0, 0xFFFF):04X} PID:{random.randint(0, 0xFFFF):04X} "
            f"EP0:{random.choice([8, 16, 32, 64])}B State:CONFIGURED{RESET}"
        )
        time.sleep(SPEED_EVENT_PAUSE)

    elif event == "wmi_query":
        wmi_class = random.choice(["Core_System", "Process_Table", "Volume_Map", "Service_Node"])
        print(
            f"{CYAN}[MGMT_QUERY] CoreServices::ExecQuery -> SELECT * FROM {wmi_class} "
            f"Enum:0x{random.randint(0x100, 0xFFFF):X} HRESULT:0x00000000{RESET}"
        )
        time.sleep(SPEED_EVENT_PAUSE)

    elif event == "dep_mitigation":
        print(
            f"{LIGHT_RED}[DEP_GUARD] NX fault at {address} PTE:0x{random.getrandbits(48):012X} "
            f"Policy:PROCESS_DEP_ENABLE -> EXECUTION_BLOCKED{RESET}"
        )
        safe_beep(400, 100)
        time.sleep(0.1)

    elif event == "aslr_shift":
        print(
            f"{GREEN}[ASLR_RAND] {random.choice(MODULES)} Base:{address} "
            f"Delta:+0x{random.randint(0x10, 0xFFF):X}0000 Entropy:{random.randint(8, 32)}b{RESET}"
        )
        time.sleep(0.04)

    elif event == "handle_close":
        print(
            f"{DARK_GRAY}[HANDLE_CLR] Table:0x{random.randint(10, 500):X} Object:{address} "
            f"Refs:{random.randint(0, 2)} Type:{random.choice(['File', 'Event', 'Section', 'Key'])}{RESET}"
        )
        time.sleep(0.01)

    elif event == "irq_balance":
        print(
            f"{WHITE}[IRQ_LINE] Vector:0x{random.randint(0x30, 0xEF):02X} IRQL:{random.randint(2, 15)} "
            f"CPU_{random.randint(0, 31)} Affinity:0x{random.getrandbits(32):08X} DPC:{random.randint(0, 1)}{RESET}"
        )
        time.sleep(SPEED_EVENT_PAUSE)

    elif event == "io_flush":
        print(
            f"{BLUE}[IO_FLUSH] \\Device\\HarddiskVolume{random.randint(1, 4)} Offset:0x{random.getrandbits(40):010X} "
            f"Len:{random.randint(4, 1024)}KB FUA:{random.randint(0, 1)} Status:0x00000000{RESET}"
        )
        time.sleep(0.03)

    elif event == "gpu_command":
        print(
            f"{MAGENTA}[GPU_DMA] Engine:{random.choice(['3D', 'COPY', 'COMPUTE', 'VIDEO'])} "
            f"Ctx:0x{random.getrandbits(32):08X} Fence:{random.randint(1000, 999999)} "
            f"VA:{address} QueueDepth:{random.randint(1, 128)}{RESET}"
        )
        time.sleep(0.02)

    elif event == "dxgk_present":
        print(
            f"{LIGHT_CYAN}[DXGKRNL] PresentHistoryToken:0x{random.getrandbits(48):012X} "
            f"VidPnSource:{random.randint(0, 3)} Flip:{random.choice(['MPO', 'HW', 'COMPOSED'])} "
            f"SyncInterval:{random.randint(0, 4)}{RESET}"
        )
        time.sleep(0.03)

    elif event == "dns_query":
        label = "".join(random.choice("abcdefghijklmnopqrstuvwxyz0123456789") for _ in range(random.randint(8, 18)))
        print(
            f"{CYAN}[DNS_CACHE] QNAME:{label}.{random.choice(['sys', 'node', 'edge', 'local'])} "
            f"TYPE:{random.choice(['A', 'AAAA', 'PTR', 'SRV'])} TXID:0x{random.randint(0, 0xFFFF):04X} "
            f"TTL:{random.randint(1, 86400)} RCODE:NOERROR{RESET}"
        )
        time.sleep(SPEED_EVENT_PAUSE)

    elif event == "tcp_retransmit":
        print(
            f"{YELLOW}[TCP_RTX] {random_ip()}:{random.randint(1024, 65535)} -> "
            f"{random_ip()}:{random.randint(20, 9000)} SEQ:{random.getrandbits(32)} "
            f"ACK:{random.getrandbits(32)} RTO:{random.randint(80, 1200)}ms CWND:{random.randint(2, 256)}{RESET}"
        )
        time.sleep(0.04)

    elif event == "arp_cache":
        print(
            f"{GREEN}[ARP_TABLE] IF:{random.choice(INTERFACES)} IPv4:10.{random.randint(0, 255)}."
            f"{random.randint(0, 255)}.{random.randint(1, 254)} -> L2:{generate_mac()} "
            f"State:{random.choice(['REACHABLE', 'STALE', 'PROBE'])}{RESET}"
        )
        time.sleep(0.03)

    elif event == "socket_bind":
        print(
            f"{DARK_GRAY}[WSK_SOCKET] AFD:0x{random.randint(0x100, 0xFFFF):X} PID:{pid} "
            f"AF:{random.choice(['INET', 'INET6'])} SOCK:{random.choice(['STREAM', 'DGRAM'])} "
            f"LocalPort:{random.randint(1024, 65535)} Handle:0x{random.randint(0x100, 0xFFFF):X}{RESET}"
        )
        time.sleep(0.02)

    elif event == "acpi_method":
        method = random.choice(["_PTS", "_WAK", "_DSM", "_STA", "_CRS", "_PRW"])
        print(
            f"{WHITE}[ACPI_AML] Eval:{method} Scope:\\_SB.PCI0 Arg0:0x{random.randint(0, 255):02X} "
            f"PkgLen:{random.randint(8, 512)} Result:AE_OK ThermalZone:{random.randint(0, 7)}{RESET}"
        )
        time.sleep(SPEED_EVENT_PAUSE)

    elif event == "tpm_quote":
        print(
            f"{MAGENTA}[TPM2_QUOTE] PCR:{random.choice([0, 2, 4, 7, 11])} "
            f"Digest:{random.getrandbits(128):032X} Nonce:{random.getrandbits(64):016X} "
            f"Alg:{random.choice(['SHA256', 'SHA384'])} RC:0x000{RESET}"
        )
        time.sleep(0.06)

    elif event == "kerberos_ticket":
        print(
            f"{YELLOW}[KERBEROS] LUID:0x{random.getrandbits(48):012X} "
            f"Ticket:{random.choice(['TGT', 'TGS', 'AP_REQ'])} EType:{random.choice(['AES256', 'AES128'])} "
            f"Kvno:{random.randint(1, 19)} CacheSlot:{random.randint(0, 255)}{RESET}"
        )
        time.sleep(SPEED_EVENT_PAUSE)

    elif event == "smb_session":
        print(
            f"{LIGHT_CYAN}[SMB3] SessionID:0x{random.getrandbits(64):016X} TreeID:0x{random.getrandbits(32):08X} "
            f"Credit:{random.randint(1, 512)} Dialect:3.1.1 Cmd:{random.choice(['READ', 'WRITE', 'QUERY_INFO', 'ECHO'])} "
            f"MID:{random.randint(1, 999999)}{RESET}"
        )
        time.sleep(0.04)

    elif event == "defender_scan":
        sig = random.getrandbits(64)
        print(
            f"{GREEN}[AMSI_SCAN] ContentID:0x{random.getrandbits(32):08X} Sig:{sig:016X} "
            f"Engine:{random.randint(1, 9)}.{random.randint(100, 999)} "
            f"Verdict:{random.choice(['CLEAN', 'ALLOW', 'NO_THREAT'])} ScanTime:{random.randint(1, 60)}ms{RESET}"
        )
        time.sleep(0.05)

    elif event == "boot_entropy":
        print(
            f"{BLUE}[BOOT_RNG] EntropyBlock:{random.getrandbits(128):032X} "
            f"Source:{random.choice(['TPM', 'RDRAND', 'TSC_JITTER', 'EFI_RNG'])} "
            f"PoolIndex:{random.randint(0, 31)} MixRounds:{random.randint(4, 64)}{RESET}"
        )
        time.sleep(0.02)

    elif event == "uefi_variable":
        print(
            f"{WHITE}[UEFI_VAR] GUID:{generate_guid()} Attr:0x{random.randint(1, 0x3F):08X} "
            f"DataSize:{random.randint(8, 4096)} Monotonic:{random.getrandbits(32)} "
            f"Status:EFI_SUCCESS{RESET}"
        )
        time.sleep(0.05)

    elif event == "tlb_shootdown":
        print(
            f"{RED}[TLB_IPI] VA:{address} PCID:{random.randint(0, 4095)} "
            f"CPU_MASK:0x{random.getrandbits(32):08X} INVPCID:{random.randint(0, 3)} "
            f"IPI_Vector:0x{random.randint(0xD0, 0xEF):02X}{RESET}"
        )
        time.sleep(0.015)

    elif event == "cache_miss":
        print(
            f"{DARK_GRAY}[PMU_CACHE] Core:{random.randint(0, 31)} L{random.choice([1, 2, 3])}_MISS "
            f"IP:{address} Set:0x{random.randint(0, 0xFFF):03X} Way:{random.randint(0, 15)} "
            f"Latency:{random.randint(12, 380)}cy{RESET}"
        )
        time.sleep(0.015)

    elif event == "branch_predictor":
        print(
            f"{DARK_GRAY}[CPU_BPU] RIP:{address} BranchID:0x{random.randint(0, 0xFFFF):04X} "
            f"Pred:{random.choice(['TAKEN', 'NOT_TAKEN'])} Actual:{random.choice(['TAKEN', 'NOT_TAKEN'])} "
            f"BTBSet:{random.randint(0, 4095)}{RESET}"
        )
        time.sleep(0.012)

    elif event == "numa_migrate":
        print(
            f"{CYAN}[NUMA_MM] PFN:0x{random.randint(0x1000, 0xFFFFFF):X} "
            f"Node:{random.randint(0, 3)} -> Node:{random.randint(0, 3)} Pages:{random.randint(1, 512)} "
            f"Policy:{random.choice(['LOCAL', 'INTERLEAVE', 'PREFERRED'])}{RESET}"
        )
        time.sleep(0.03)

    elif event == "clock_interrupt":
        print(
            f"{WHITE}[HAL_CLOCK] Vector:0x{random.randint(0x30, 0xEF):02X} TSC:{random.getrandbits(56):014X} "
            f"Deadline:{random.getrandbits(48):012X} CPU:{random.randint(0, 31)} "
            f"Drift:{random.uniform(-0.80, 0.80):+.3f}us{RESET}"
        )
        time.sleep(0.015)

    elif event == "power_state":
        print(
            f"{BLUE}[PO_FX] Device:0x{random.randint(0x1000, 0xFFFF):X} "
            f"Dx:{random.randint(0, 3)} Sx:{random.randint(0, 5)} IdleState:F{random.randint(0, 3)} "
            f"Latency:{random.randint(1, 5000)}us IRP:0x{random.getrandbits(32):08X}{RESET}"
        )
        time.sleep(0.04)

    elif event == "dpc_queue":
        print(
            f"{LIGHT_RED}[KDPC_QUEUE] CPU:{random.randint(0, 31)} Dpc:0x{random.getrandbits(48):012X} "
            f"Routine:{address} Importance:{random.choice(['LOW', 'MEDIUM', 'HIGH'])} "
            f"Depth:{random.randint(0, 128)}{RESET}"
        )
        time.sleep(0.02)

    elif event == "object_manager":
        print(
            f"{YELLOW}[OB_MANAGER] Type:{random.choice(['Process', 'Thread', 'Section', 'Event', 'Directory'])} "
            f"Object:{address} Handle:0x{random.randint(0x100, 0xFFFF):X} "
            f"PtrRefs:{random.randint(1, 128)} HandleRefs:{random.randint(0, 64)}{RESET}"
        )
        time.sleep(0.025)

    elif event == "alpc_message":
        print(
            f"{CYAN}[ALPC_PORT] Port:\\RPC Control\\{generate_guid()[1:9]} MsgID:{random.randint(1, 999999)} "
            f"Len:{random.randint(32, 4096)} PID:{pid} View:0x{random.getrandbits(48):012X} "
            f"Flags:0x{random.randint(0, 0xFFFF):04X}{RESET}"
        )
        time.sleep(0.03)

    elif event == "named_pipe":
        print(
            f"{MAGENTA}[NPFS_PIPE] \\Device\\NamedPipe\\{random.choice(['lsass', 'srvsvc', 'wkssvc', 'atsvc'])}."
            f"{random.randint(100, 9999)} Instance:{random.randint(0, 16)} "
            f"Mode:{random.choice(['MESSAGE', 'BYTE'])} Quota:{random.randint(4096, 65536)}{RESET}"
        )
        time.sleep(0.035)

    elif event == "file_journal":
        print(
            f"{GREEN}[NTFS_USN] USN:0x{random.getrandbits(64):016X} FRN:0x{random.getrandbits(64):016X} "
            f"Reason:0x{random.randint(1, 0xFFFF):08X} Source:0x{random.randint(0, 0xFF):04X} "
            f"JournalID:{random.getrandbits(48):012X}{RESET}"
        )
        time.sleep(0.025)

    elif event == "volume_shadow":
        print(
            f"{WHITE}[VOLSNAP] ShadowID:{generate_guid()} DiffArea:{random.randint(64, 8192)}MB "
            f"Block:0x{random.getrandbits(48):012X} Bitmap:{random.randint(0, 100)}% "
            f"State:{random.choice(['ACTIVE', 'COPY_ON_WRITE', 'FLUSH'])}{RESET}"
        )
        time.sleep(0.05)

    elif event == "reparse_point":
        print(
            f"{BLUE}[REPARSE] Tag:0x{random.choice([0xA0000003, 0xA000000C, 0x8000001B]):08X} "
            f"FileID:0x{random.getrandbits(64):016X} SubstituteNameLen:{random.randint(8, 240)} "
            f"Result:STATUS_REPARSE{RESET}"
        )
        time.sleep(0.03)

    elif event == "minifilter":
        print(
            f"{LIGHT_CYAN}[FLT_MGR] Altitude:{random.randint(100000, 499999)}.{random.randint(1, 999)} "
            f"Op:{random.choice(['IRP_MJ_CREATE', 'IRP_MJ_READ', 'IRP_MJ_WRITE', 'IRP_MJ_CLEANUP'])} "
            f"Instance:0x{random.getrandbits(32):08X} PreOp:{random.choice(['SUCCESS', 'PENDING'])}{RESET}"
        )
        time.sleep(0.035)

    elif event == "code_integrity":
        print(
            f"{YELLOW}[CI_VERIFY] Image:{random.choice(MODULES)} SHA256:{random.getrandbits(128):032X} "
            f"Policy:{random.randint(1, 15)} Signing:{random.choice(['ROOT_CA', 'CORE_SIGNED', 'TRUSTED_STORE'])} "
            f"Result:STATUS_SUCCESS{RESET}"
        )
        time.sleep(0.06)

    elif event == "heap_segment":
        print(
            f"{RED}[SEG_HEAP] Heap:0x{random.getrandbits(48):012X} Segment:0x{random.getrandbits(48):012X} "
            f"Bucket:{random.randint(0, 255)} Block:{random.randint(16, 65536)}B "
            f"LFH:{random.choice(['ON', 'OFF'])} Cookie:0x{random.getrandbits(32):08X}{RESET}"
        )
        time.sleep(0.02)

    elif event == "wow64_transition":
        print(
            f"{MAGENTA}[WOW64_GATE] PID:{pid} x86_EIP:0x{random.getrandbits(32):08X} -> "
            f"x64_RIP:{address} Service:0x{random.randint(0, 0x1FFF):04X} "
            f"CS:0x33 SS:0x2B Gate:HeavenTransition{RESET}"
        )
        time.sleep(0.025)

    elif event in LORE_EVENTS:
        emit_lore_event(event)

    elif event in EXTRA_EVENT_TO_FAMILY:
        emit_extra_event(event)

    else:
        raise RuntimeError(f"Unknown event type: {event}")


def run_advanced_debugger():
    if CONSOLE_ACCESS_INTRO:
        run_console_access_intro()
    if CINEMATIC_INTRO:
        run_story_intro()
    else:
        draw_progress_bar()
    threading.Thread(target=key_listener, daemon=True).start()
    next_super_event = time.monotonic() + random.uniform(SUPER_EVENT_FIRST_MIN, SUPER_EVENT_FIRST_MAX)

    try:
        while RUNNING.is_set():
            wait_if_paused()
            update_flow_mode()
            decay_defcon()

            now = time.monotonic()
            if now >= next_super_event:
                run_super_event()
                next_super_event = time.monotonic() + random.uniform(
                    SUPER_EVENT_MIN_DELAY,
                    SUPER_EVENT_MAX_DELAY,
                )
                continue

            roll = random.random()
            if roll < GLITCH_CHANCE:
                if DEFCON == 0 and random.random() < 0.30:
                    set_defcon(1, "stream corruption")
                glitch_burst()
            elif roll < GLITCH_CHANCE + CHAIN_CHANCE:
                run_event_chain()
            else:
                emit_event(random.choice(EVENTS))
    except KeyboardInterrupt:
        RUNNING.clear()
        PAUSED.clear()
        print(f"\n\n{BOLD}{RED}[!] ТЕРМИНАЛ ОТКЛЮЧЕН ОПЕРАТОРОМ.{RESET}")


if __name__ == "__main__":
    if os.name == "nt":
        os.system("chcp 65001 > nul")
        os.system("")
    clear_console()
    run_advanced_debugger()
