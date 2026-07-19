<script lang="ts">
    import StatusBadge from '../components/StatusBadge.svelte';
    import { Activity, BarChart3 } from '@lucide/svelte';

    const usageHighlights = [
        { label: 'Active Machines', value: '9', delta: '+2 this week' },
        { label: 'Uploads (7d)', value: '54', delta: '+12% WoW' },
        { label: 'Rollbacks (7d)', value: '3', delta: '-1 vs last week' },
        { label: 'Avg. Approval', value: '18m', delta: '-6 min' },
    ];

    const activityTimeline = [
        { title: 'Upload completed', detail: 'pump_housing_v2.nc → Machine 101', meta: 'Today, 09:42', status: 'success' as const },
        { title: 'Rollback executed', detail: 'turbine_blade_v1.nc → version 2', meta: 'Today, 08:15', status: 'warning' as const },
        { title: 'Comparison generated', detail: 'valve_seal_v2.gcode vs v3', meta: 'Yesterday, 16:10', status: 'info' as const },
        { title: 'Access updated', detail: 'Operator role added for A. Rivera', meta: 'Yesterday, 14:05', status: 'info' as const },
    ];

    const auditReports = [
        { name: 'Weekly Compliance Snapshot', owner: 'QA Team', date: 'May 30, 2026', status: 'Ready' },
        { name: 'Machine 101 Change Log', owner: 'Ops Lead', date: 'May 28, 2026', status: 'Ready' },
        { name: 'Rollback Incident Review', owner: 'Admin', date: 'May 24, 2026', status: 'In Review' },
    ];

    const usageSeries = [
        { label: 'Mon', value: 28 }, { label: 'Tue', value: 42 }, { label: 'Wed', value: 35 },
        { label: 'Thu', value: 54 }, { label: 'Fri', value: 48 }, { label: 'Sat', value: 22 }, { label: 'Sun', value: 31 },
    ];

    const maxValue = Math.max(...usageSeries.map(d => d.value));
</script>

<div class="analytics-page">
    <div class="card">
        <div class="card-header">
            <h3>Usage Analytics</h3>
            <span class="card-action">Last 7 days</span>
        </div>
        <div class="stat-grid">
            {#each usageHighlights as stat}
                <div class="stat-card">
                    <span class="stat-label">{stat.label}</span>
                    <span class="stat-value">{stat.value}</span>
                    <span class="stat-delta">{stat.delta}</span>
                </div>
            {/each}
        </div>

        <div class="chart-section">
            <h4>Upload Frequency</h4>
            <div class="mini-chart">
                {#each usageSeries as day}
                    <div class="bar-col" title="{day.label}: {day.value}">
                        <div class="bar-fill" style="height: {(day.value / maxValue) * 100}%"></div>
                        <span class="bar-label">{day.label}</span>
                    </div>
                {/each}
            </div>
        </div>
    </div>

    <div class="card">
        <div class="card-header">
            <h3>Activity Timeline</h3>
            <span class="card-action">Past 48 hours</span>
        </div>
        <div class="timeline">
            {#each activityTimeline as item}
                <div class="timeline-item">
                    <span class="timeline-dot {item.status}"></span>
                    <div>
                        <p class="tl-title">{item.title}</p>
                        <p class="tl-detail">{item.detail}</p>
                        <p class="tl-meta">{item.meta}</p>
                    </div>
                </div>
            {/each}
        </div>
    </div>

    <div class="card">
        <div class="card-header">
            <h3>Audit Reports</h3>
            <span class="card-action">Export ready</span>
        </div>
        <div class="table-container">
            <table class="data-table">
                <thead>
                    <tr><th>Report</th><th>Owner</th><th>Date</th><th>Status</th></tr>
                </thead>
                <tbody>
                    {#each auditReports as report}
                        <tr>
                            <td class="report-name">{report.name}</td>
                            <td class="meta-text">{report.owner}</td>
                            <td class="meta-text">{report.date}</td>
                            <td>
                                <StatusBadge variant={report.status === 'Ready' ? 'success' : 'warning'}>
                                    {report.status}
                                </StatusBadge>
                            </td>
                        </tr>
                    {/each}
                </tbody>
            </table>
        </div>
    </div>
</div>

<style>
    .analytics-page { display: grid; gap: var(--space-lg); max-width: 960px; }

    .card {
        background: var(--color-surface-1);
        border: 1px solid var(--color-hairline);
        border-radius: var(--radius-lg);
        padding: var(--space-lg);
    }
    .card-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: var(--space-lg); }
    .card-header h3 { font-size: 18px; font-weight: 600; color: var(--color-ink); margin: 0; }
    .card-action { font-size: 12px; font-weight: 600; color: var(--color-ink-subtle); }

    .stat-grid { display: grid; gap: var(--space-md); grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); margin-bottom: var(--space-lg); }
    .stat-card { background: var(--color-surface-2); border: 1px solid var(--color-hairline); border-radius: var(--radius-lg); padding: var(--space-md); display: flex; flex-direction: column; gap: var(--space-xxs); }
    .stat-label { font-size: 12px; font-weight: 500; color: var(--color-ink-subtle); text-transform: uppercase; letter-spacing: 0.06em; }
    .stat-value { font-size: 28px; font-weight: 700; color: var(--color-ink); letter-spacing: -0.6px; }
    .stat-delta { font-size: 12px; color: var(--color-ink-tertiary); }

    .chart-section h4 { font-size: 13px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.06em; color: var(--color-ink-subtle); margin: 0 0 var(--space-md); }

    .mini-chart { display: grid; grid-template-columns: repeat(7, 1fr); gap: var(--space-xs); align-items: end; height: 160px; }
    .bar-col { display: flex; flex-direction: column; align-items: center; gap: var(--space-xs); height: 100%; justify-content: flex-end; }
    .bar-fill { width: 100%; max-width: 24px; border-radius: var(--radius-sm) var(--radius-sm) 0 0; background: linear-gradient(180deg, var(--color-primary), var(--color-primary-focus)); min-height: 4px; transition: height var(--transition-slow); }
    .bar-col:hover .bar-fill { background: linear-gradient(180deg, var(--color-primary-hover), var(--color-primary)); }
    .bar-label { font-size: 11px; color: var(--color-ink-tertiary); font-weight: 500; }

    .timeline { display: flex; flex-direction: column; gap: var(--space-md); }
    .timeline-item { display: grid; grid-template-columns: 12px 1fr; gap: var(--space-sm); }
    .timeline-dot { width: 10px; height: 10px; border-radius: var(--radius-full); margin-top: 5px; background: var(--color-ink-tertiary); }
    .timeline-dot.success { background: var(--color-success); box-shadow: 0 0 0 4px var(--color-success-subtle); }
    .timeline-dot.warning { background: var(--color-warning); box-shadow: 0 0 0 4px var(--color-warning-subtle); }
    .timeline-dot.info { background: var(--color-primary); box-shadow: 0 0 0 4px rgba(94, 106, 210, 0.15); }
    .tl-title { font-size: 14px; font-weight: 600; color: var(--color-ink); margin: 0; }
    .tl-detail { font-size: 13px; color: var(--color-ink-muted); margin: 2px 0 0; }
    .tl-meta { font-size: 12px; color: var(--color-ink-tertiary); margin: 4px 0 0; }

    .table-container { overflow-x: auto; }
    .data-table { width: 100%; border-collapse: collapse; }
    .data-table th { text-align: left; font-size: 12px; font-weight: 600; color: var(--color-ink-tertiary); text-transform: uppercase; letter-spacing: 0.04em; padding: var(--space-sm); border-bottom: 1px solid var(--color-hairline); }
    .data-table td { padding: var(--space-sm); border-bottom: 1px solid var(--color-hairline); font-size: 14px; }
    .report-name { font-weight: 500; color: var(--color-ink); }
    .meta-text { color: var(--color-ink-subtle); }
</style>
