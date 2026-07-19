<script lang="ts">
    import { user } from '../authStore';
    import StatusBadge from '../components/StatusBadge.svelte';
    import { Activity, Upload, ArrowUpRight, TrendingUp, RotateCcw, Clock } from '@lucide/svelte';

    export let onNavigate: (tab: string) => void = () => {};

    const usageHighlights = [
        { label: 'Active Machines', value: '9', delta: '+2 this week', trend: 'up' },
        { label: 'Uploads (7d)', value: '54', delta: '+12% WoW', trend: 'up' },
        { label: 'Rollbacks (7d)', value: '3', delta: '-1 vs last week', trend: 'down' },
        { label: 'Avg. Approval', value: '18m', delta: '-6 min', trend: 'down' },
    ];

    const activityTimeline = [
        { title: 'Upload completed', detail: 'pump_housing_v2.nc → Machine 101', meta: 'Today, 09:42', status: 'success' as const },
        { title: 'Rollback executed', detail: 'turbine_blade_v1.nc → version 2', meta: 'Today, 08:15', status: 'warning' as const },
        { title: 'Comparison generated', detail: 'valve_seal_v2.gcode vs v3', meta: 'Yesterday, 16:10', status: 'info' as const },
        { title: 'Access updated', detail: 'Operator role added for A. Rivera', meta: 'Yesterday, 14:05', status: 'info' as const },
    ];

    const machines = [
        { id: '101', name: 'Pump Housing Cell', type: '3-Axis CNC Mill', status: 'Online' as const, programs: 18, location: 'Building A - Bay 1' },
        { id: '102', name: 'Turbine Blade Cell', type: '5-Axis CNC Mill', status: 'Idle' as const, programs: 22, location: 'Building A - Bay 2' },
        { id: '103', name: 'Valve Seal Cell', type: 'CNC Lathe', status: 'Online' as const, programs: 11, location: 'Building B - Bay 1' },
    ];

    const usageSeries = [
        { label: 'Mon', value: 28 },
        { label: 'Tue', value: 42 },
        { label: 'Wed', value: 35 },
        { label: 'Thu', value: 54 },
        { label: 'Fri', value: 48 },
        { label: 'Sat', value: 22 },
        { label: 'Sun', value: 31 },
    ];

    const maxValue = Math.max(...usageSeries.map(d => d.value));

    function statusVariant(status: string): 'success' | 'warning' | 'error' | 'neutral' {
        switch (status) {
            case 'Online': return 'success';
            case 'Maintenance': return 'warning';
            case 'Offline': return 'error';
            default: return 'neutral';
        }
    }
</script>

<div class="overview">
    <!-- Hero Stats -->
    <div class="card hero-card">
        <div class="card-header">
            <div>
                <span class="eyebrow">AutoVault Command Center</span>
                <h3>Enterprise Snapshot</h3>
            </div>
            <StatusBadge variant="success" dot>Systems Normal</StatusBadge>
        </div>
        <div class="stat-grid">
            {#each usageHighlights as stat}
                <div class="stat-card">
                    <span class="stat-label">{stat.label}</span>
                    <span class="stat-value">{stat.value}</span>
                    <span class="stat-delta" class:positive={stat.trend === 'up'} class:negative={stat.trend === 'down'}>
                        {stat.delta}
                    </span>
                </div>
            {/each}
        </div>
    </div>

    <div class="two-col">
        <!-- Activity Feed -->
        <div class="card">
            <div class="card-header">
                <h3>Latest Activity</h3>
                <span class="card-action">
                    <Activity size={14} />
                    Live feed
                </span>
            </div>
            <div class="timeline">
                {#each activityTimeline as item}
                    <div class="timeline-item">
                        <span class="timeline-dot {item.status}"></span>
                        <div class="timeline-content">
                            <p class="timeline-title">{item.title}</p>
                            <p class="timeline-detail">{item.detail}</p>
                            <p class="timeline-meta">{item.meta}</p>
                        </div>
                    </div>
                {/each}
            </div>
        </div>

        <!-- Sparkline Chart -->
        <div class="card">
            <div class="card-header">
                <h3>Upload Trend</h3>
                <span class="card-action">Last 7 days</span>
            </div>
            <div class="mini-chart">
                {#each usageSeries as day}
                    <div class="bar-col" title="{day.label}: {day.value} uploads">
                        <div class="bar-fill" style="height: {(day.value / maxValue) * 100}%"></div>
                        <span class="bar-label">{day.label}</span>
                    </div>
                {/each}
            </div>
        </div>
    </div>

    <!-- Quick Access Machines -->
    <div class="card">
        <div class="card-header">
            <h3>Machine Fleet</h3>
            <button class="link-btn" on:click={() => onNavigate('machines')}>
                View all <ArrowUpRight size={14} />
            </button>
        </div>
        <div class="machine-grid">
            {#each machines as machine}
                <div class="machine-card">
                    <div class="machine-header">
                        <span class="machine-name">{machine.name}</span>
                        <StatusBadge variant={statusVariant(machine.status)} dot>{machine.status}</StatusBadge>
                    </div>
                    <span class="machine-type">{machine.type}</span>
                    <div class="machine-footer">
                        <span>{machine.programs} programs</span>
                        <span>{machine.location}</span>
                    </div>
                </div>
            {/each}
        </div>
    </div>
</div>

<style>
    .overview {
        display: grid;
        gap: var(--space-lg);
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
        letter-spacing: -0.3px;
    }

    .eyebrow {
        display: block;
        font-size: 12px;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: var(--color-ink-subtle);
        margin-bottom: var(--space-xxs);
    }

    .card-action {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        font-size: 12px;
        font-weight: 600;
        color: var(--color-ink-subtle);
    }

    .stat-grid {
        display: grid;
        gap: var(--space-md);
        grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    }

    .stat-card {
        background: var(--color-surface-2);
        border: 1px solid var(--color-hairline);
        border-radius: var(--radius-lg);
        padding: var(--space-md);
        display: flex;
        flex-direction: column;
        gap: var(--space-xxs);
    }

    .stat-label {
        font-size: 12px;
        font-weight: 500;
        color: var(--color-ink-subtle);
        text-transform: uppercase;
        letter-spacing: 0.06em;
    }

    .stat-value {
        font-size: 28px;
        font-weight: 700;
        color: var(--color-ink);
        letter-spacing: -0.6px;
        line-height: 1.1;
    }

    .stat-delta {
        font-size: 12px;
        color: var(--color-ink-tertiary);
    }

    .stat-delta.positive { color: var(--color-success); }
    .stat-delta.negative { color: var(--color-ink-subtle); }

    .two-col {
        display: grid;
        gap: var(--space-lg);
        grid-template-columns: 1fr 1fr;
    }

    /* Timeline */
    .timeline {
        display: flex;
        flex-direction: column;
        gap: var(--space-md);
    }

    .timeline-item {
        display: grid;
        grid-template-columns: 12px 1fr;
        gap: var(--space-sm);
    }

    .timeline-dot {
        width: 10px;
        height: 10px;
        border-radius: var(--radius-full);
        margin-top: 5px;
        background: var(--color-ink-tertiary);
    }

    .timeline-dot.success {
        background: var(--color-success);
        box-shadow: 0 0 0 4px var(--color-success-subtle);
    }

    .timeline-dot.warning {
        background: var(--color-warning);
        box-shadow: 0 0 0 4px var(--color-warning-subtle);
    }

    .timeline-dot.info {
        background: var(--color-primary);
        box-shadow: 0 0 0 4px rgba(94, 106, 210, 0.15);
    }

    .timeline-title {
        font-size: 14px;
        font-weight: 600;
        color: var(--color-ink);
        margin: 0;
    }

    .timeline-detail {
        font-size: 13px;
        color: var(--color-ink-muted);
        margin: 2px 0 0;
    }

    .timeline-meta {
        font-size: 12px;
        color: var(--color-ink-tertiary);
        margin: 4px 0 0;
    }

    /* Mini chart */
    .mini-chart {
        display: grid;
        grid-template-columns: repeat(7, 1fr);
        gap: var(--space-xs);
        align-items: end;
        height: 180px;
        padding-top: var(--space-md);
    }

    .bar-col {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: var(--space-xs);
        height: 100%;
        justify-content: flex-end;
    }

    .bar-fill {
        width: 100%;
        max-width: 24px;
        border-radius: var(--radius-sm) var(--radius-sm) 0 0;
        background: linear-gradient(180deg, var(--color-primary), var(--color-primary-focus));
        transition: height var(--transition-slow);
        min-height: 4px;
    }

    .bar-col:hover .bar-fill {
        background: linear-gradient(180deg, var(--color-primary-hover), var(--color-primary));
    }

    .bar-label {
        font-size: 11px;
        color: var(--color-ink-tertiary);
        font-weight: 500;
    }

    /* Machine Grid */
    .machine-grid {
        display: grid;
        gap: var(--space-md);
        grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
    }

    .machine-card {
        padding: var(--space-md);
        border: 1px solid var(--color-hairline);
        border-radius: var(--radius-lg);
        background: var(--color-surface-2);
        display: flex;
        flex-direction: column;
        gap: var(--space-xs);
        transition: border-color var(--transition-fast);
    }

    .machine-card:hover {
        border-color: var(--color-hairline-strong);
    }

    .machine-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: var(--space-xs);
    }

    .machine-name {
        font-size: 14px;
        font-weight: 600;
        color: var(--color-ink);
    }

    .machine-type {
        font-size: 13px;
        color: var(--color-ink-subtle);
    }

    .machine-footer {
        display: flex;
        flex-direction: column;
        gap: 2px;
        font-size: 12px;
        color: var(--color-ink-tertiary);
        margin-top: var(--space-xxs);
    }

    .link-btn {
        display: inline-flex;
        align-items: center;
        gap: 4px;
        background: none;
        border: none;
        color: var(--color-primary);
        font-size: 13px;
        font-weight: 600;
        cursor: pointer;
        padding: 0;
        transition: color var(--transition-fast);
    }

    .link-btn:hover {
        color: var(--color-primary-hover);
    }

    @media (max-width: 768px) {
        .two-col {
            grid-template-columns: 1fr;
        }
    }
</style>
