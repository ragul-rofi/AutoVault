<script lang="ts">
    import StatusBadge from '../components/StatusBadge.svelte';
    import { Activity, Upload, ArrowUpRight, Cpu, HardDrive, ShieldCheck, Zap, ArrowRight, Clock, FileText } from '@lucide/svelte';

    export let onNavigate: (tab: string) => void = () => {};

    const liveStats = [
        { label: 'Online Fleet', value: '3 / 4', delta: '75% Active', trend: 'up' },
        { label: 'Managed Programs', value: '51', delta: '+4 this month', trend: 'up' },
        { label: 'System Uptime', value: '99.98%', delta: '0 outages', trend: 'up' },
        { label: 'Storage Usage', value: '1.42 GB', delta: 'MinIO Vault', trend: 'up' },
    ];

    const liveFeed = [
        { title: 'New Program Upload', detail: 'pump_housing_v2.nc uploaded to Machine 101', time: '12 mins ago', type: 'success' as const },
        { title: 'Rollback Triggered', detail: 'turbine_blade.nc reverted to v1 on Machine 102', time: '1 hour ago', type: 'warning' as const },
        { title: 'SHA-256 Hash Verified', detail: 'valve_seal_v2.gcode integrity checksum passed', time: '3 hours ago', type: 'info' as const },
        { title: 'Machine Status Change', detail: 'Precision Lathe (103) status updated to Online', time: '5 hours ago', type: 'info' as const },
    ];

    const fleetStatus = [
        { id: '101', name: 'CNC Milling Center', program: 'pump_housing.nc (v2)', status: 'Online' as const, operator: 'John Doe' },
        { id: '102', name: 'PLC Assembly Line', program: 'turbine_blade.nc (v3)', status: 'Idle' as const, operator: 'Jane Smith' },
        { id: '103', name: 'Precision Lathe', program: 'valve_seal.gcode (v2)', status: 'Online' as const, operator: 'Bob Johnson' },
        { id: '104', name: 'Seal Calibration Cell', program: 'bracket_arm.cnc (v4)', status: 'Maintenance' as const, operator: 'A. Rivera' },
    ];

    function statusVariant(status: string): 'success' | 'warning' | 'error' | 'neutral' {
        switch (status) {
            case 'Online': return 'success';
            case 'Maintenance': return 'warning';
            case 'Offline': return 'error';
            default: return 'neutral';
        }
    }
</script>

<div class="overview-page">
    <!-- Operational Command Center Hero -->
    <div class="card hero-card">
        <div class="card-header">
            <div>
                <span class="eyebrow">Real-Time Operations</span>
                <h3>AutoVault Command Center</h3>
            </div>
            <StatusBadge variant="success" dot>Live System Health: 100%</StatusBadge>
        </div>

        <div class="stat-grid">
            {#each liveStats as stat}
                <div class="stat-card">
                    <span class="stat-label">{stat.label}</span>
                    <span class="stat-value">{stat.value}</span>
                    <span class="stat-delta">{stat.delta}</span>
                </div>
            {/each}
        </div>
    </div>

    <!-- Quick Operations Hub -->
    <div class="card">
        <div class="card-header">
            <h3>Quick Operations Hub</h3>
        </div>
        <div class="quick-launchers">
            <button class="launcher-card" on:click={() => onNavigate('upload')}>
                <div class="launcher-icon brand"><Upload size={20} /></div>
                <div class="launcher-text">
                    <span class="launcher-title">Upload Program</span>
                    <span class="launcher-sub">Deploy .nc, .gcode, .cnc files</span>
                </div>
                <ArrowRight size={16} class="arrow" />
            </button>

            <button class="launcher-card" on:click={() => onNavigate('view')}>
                <div class="launcher-icon info"><FileText size={20} /></div>
                <div class="launcher-text">
                    <span class="launcher-title">File Browser</span>
                    <span class="launcher-sub">Inspect versions & preview</span>
                </div>
                <ArrowRight size={16} class="arrow" />
            </button>

            <button class="launcher-card" on:click={() => onNavigate('compare')}>
                <div class="launcher-icon warning"><Zap size={20} /></div>
                <div class="launcher-text">
                    <span class="launcher-title">Compare Versions</span>
                    <span class="launcher-sub">Side-by-side code diff</span>
                </div>
                <ArrowRight size={16} class="arrow" />
            </button>

            <button class="launcher-card" on:click={() => onNavigate('machines')}>
                <div class="launcher-icon success"><Cpu size={20} /></div>
                <div class="launcher-text">
                    <span class="launcher-title">Machine Fleet</span>
                    <span class="launcher-sub">Sync machines & programs</span>
                </div>
                <ArrowRight size={16} class="arrow" />
            </button>
        </div>
    </div>

    <div class="two-col">
        <!-- Live Activity Stream -->
        <div class="card">
            <div class="card-header">
                <h3>Live System Feed</h3>
                <span class="card-action"><Activity size={14} /> Realtime</span>
            </div>
            <div class="feed-list">
                {#each liveFeed as item}
                    <div class="feed-item">
                        <span class="feed-dot {item.type}"></span>
                        <div class="feed-content">
                            <p class="feed-title">{item.title}</p>
                            <p class="feed-detail">{item.detail}</p>
                            <p class="feed-time"><Clock size={12} /> {item.time}</p>
                        </div>
                    </div>
                {/each}
            </div>
        </div>

        <!-- Real-Time Machine Monitor -->
        <div class="card">
            <div class="card-header">
                <h3>Active Machine Monitor</h3>
                <button class="link-btn" on:click={() => onNavigate('machines')}>
                    View Fleet <ArrowUpRight size={14} />
                </button>
            </div>
            <div class="fleet-mini-list">
                {#each fleetStatus as machine}
                    <div class="fleet-row">
                        <div class="fleet-info">
                            <span class="m-name">#{machine.id} · {machine.name}</span>
                            <span class="m-prog">{machine.program}</span>
                        </div>
                        <StatusBadge variant={statusVariant(machine.status)} dot>{machine.status}</StatusBadge>
                    </div>
                {/each}
            </div>
        </div>
    </div>
</div>

<style>
    .overview-page {
        display: grid;
        gap: var(--space-lg);
        max-width: 1040px;
    }

    .card {
        background: var(--color-surface-1);
        border: 1px solid var(--color-hairline);
        border-radius: var(--radius-lg);
        padding: var(--space-lg);
    }

    .hero-card {
        border-color: var(--color-hairline-strong);
    }

    .card-header {
        display: flex;
        align-items: flex-start;
        justify-content: space-between;
        gap: var(--space-md);
        margin-bottom: var(--space-lg);
    }

    .card-header h3 {
        font-size: 18px;
        font-weight: 600;
        color: var(--color-ink);
        margin: 0;
    }

    .eyebrow {
        display: block;
        font-size: 11px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: var(--color-primary);
        margin-bottom: 2px;
    }

    .stat-grid {
        display: grid;
        gap: var(--space-md);
        grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    }

    .stat-card {
        background: var(--color-surface-2);
        border: 1px solid var(--color-hairline);
        border-radius: var(--radius-lg);
        padding: var(--space-md);
        display: flex;
        flex-direction: column;
        gap: 2px;
    }

    .stat-label {
        font-size: 11px;
        font-weight: 600;
        color: var(--color-ink-subtle);
        text-transform: uppercase;
        letter-spacing: 0.06em;
    }

    .stat-value {
        font-size: 26px;
        font-weight: 700;
        color: var(--color-ink);
        letter-spacing: -0.5px;
    }

    .stat-delta {
        font-size: 12px;
        color: var(--color-ink-tertiary);
    }

    /* Launchers */
    .quick-launchers {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
        gap: var(--space-md);
    }

    .launcher-card {
        all: unset;
        display: flex;
        align-items: center;
        gap: var(--space-md);
        padding: var(--space-md);
        background: var(--color-surface-2);
        border: 1px solid var(--color-hairline);
        border-radius: var(--radius-lg);
        cursor: pointer;
        transition: all var(--transition-fast);
    }

    .launcher-card:hover {
        border-color: var(--color-primary);
        background: var(--color-surface-3);
    }

    .launcher-card:hover .arrow {
        transform: translateX(4px);
        color: var(--color-primary);
    }

    .launcher-icon {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 38px;
        height: 38px;
        border-radius: var(--radius-md);
        flex-shrink: 0;
    }

    .launcher-icon.brand { background: rgba(94, 106, 210, 0.12); color: var(--color-primary); }
    .launcher-icon.info { background: var(--color-info-subtle); color: var(--color-info); }
    .launcher-icon.warning { background: var(--color-warning-subtle); color: var(--color-warning); }
    .launcher-icon.success { background: var(--color-success-subtle); color: var(--color-success); }

    .launcher-text {
        flex: 1;
        display: flex;
        flex-direction: column;
    }

    .launcher-title {
        font-size: 14px;
        font-weight: 600;
        color: var(--color-ink);
    }

    .launcher-sub {
        font-size: 12px;
        color: var(--color-ink-tertiary);
    }

    .arrow {
        color: var(--color-ink-tertiary);
        transition: transform var(--transition-fast), color var(--transition-fast);
    }

    .two-col {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: var(--space-lg);
    }

    /* Feed */
    .feed-list {
        display: flex;
        flex-direction: column;
        gap: var(--space-md);
    }

    .feed-item {
        display: grid;
        grid-template-columns: 10px 1fr;
        gap: var(--space-sm);
    }

    .feed-dot {
        width: 8px;
        height: 8px;
        border-radius: var(--radius-full);
        margin-top: 6px;
    }

    .feed-dot.success { background: var(--color-success); }
    .feed-dot.warning { background: var(--color-warning); }
    .feed-dot.info { background: var(--color-primary); }

    .feed-title {
        font-size: 14px;
        font-weight: 600;
        color: var(--color-ink);
        margin: 0;
    }

    .feed-detail {
        font-size: 13px;
        color: var(--color-ink-muted);
        margin: 2px 0 0;
    }

    .feed-time {
        display: inline-flex;
        align-items: center;
        gap: 4px;
        font-size: 11px;
        color: var(--color-ink-tertiary);
        margin: 4px 0 0;
    }

    /* Fleet Mini List */
    .fleet-mini-list {
        display: flex;
        flex-direction: column;
        gap: var(--space-xs);
    }

    .fleet-row {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: var(--space-xs) var(--space-sm);
        background: var(--color-surface-2);
        border: 1px solid var(--color-hairline);
        border-radius: var(--radius-md);
    }

    .fleet-info {
        display: flex;
        flex-direction: column;
    }

    .m-name {
        font-size: 13px;
        font-weight: 600;
        color: var(--color-ink);
    }

    .m-prog {
        font-family: var(--font-mono);
        font-size: 12px;
        color: var(--color-ink-subtle);
    }

    .link-btn {
        all: unset;
        display: inline-flex;
        align-items: center;
        gap: 4px;
        font-size: 13px;
        font-weight: 600;
        color: var(--color-primary);
        cursor: pointer;
    }

    .link-btn:hover { color: var(--color-primary-hover); }

    @media (max-width: 768px) {
        .two-col { grid-template-columns: 1fr; }
    }
</style>
