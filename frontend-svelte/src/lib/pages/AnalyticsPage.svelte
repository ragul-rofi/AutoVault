<script lang="ts">
    import StatusBadge from '../components/StatusBadge.svelte';
    import { BarChart3, PieChart, ShieldCheck, TrendingUp, Calendar, FileCode, CheckCircle2, AlertOctagon } from '@lucide/svelte';

    const analyticsKPIs = [
        { label: 'Avg. Revision Depth', value: '2.8 ver/file', sub: 'Depth ratio per program' },
        { label: 'Rollback Frequency', value: '4.2%', sub: 'Low risk threshold (<5%)' },
        { label: 'Code Churn Rate', value: '+14% / ver', sub: 'Average G-Code lines modified' },
        { label: 'Hash Integrity', value: '100%', sub: 'Zero checksum corruption' },
    ];

    const fileFormatDistribution = [
        { format: '.nc (Fanuc/Haas)', count: 28, percentage: '55%', size: '820 KB', color: 'var(--color-primary)' },
        { format: '.gcode (Standard G-Code)', count: 15, percentage: '29%', size: '410 KB', color: 'var(--color-info)' },
        { format: '.cnc (Siemens Sinumerik)', count: 8, percentage: '16%', size: '240 KB', color: 'var(--color-success)' },
    ];

    const weeklyHeatmap = [
        { day: 'Mon', h08_12: 14, h12_16: 22, h16_20: 8 },
        { day: 'Tue', h08_12: 18, h12_16: 34, h16_20: 12 },
        { day: 'Wed', h08_12: 12, h12_16: 28, h16_20: 15 },
        { day: 'Thu', h08_12: 24, h12_16: 42, h16_20: 19 },
        { day: 'Fri', h08_12: 20, h12_16: 30, h16_20: 10 },
    ];

    const highChurnFiles = [
        { file: 'turbine_blade.nc', machine: 'Machine 102', revisions: 3, riskLevel: 'Low' as const },
        { file: 'pump_housing.nc', machine: 'Machine 101', revisions: 2, riskLevel: 'Optimal' as const },
        { file: 'valve_seal.gcode', machine: 'Machine 103', revisions: 2, riskLevel: 'Optimal' as const },
        { file: 'bracket_arm.cnc', machine: 'Machine 101', revisions: 4, riskLevel: 'Attention' as const },
    ];
</script>

<div class="analytics-page">
    <!-- Manufacturing Intelligence KPIs -->
    <div class="card">
        <div class="card-header">
            <div>
                <span class="eyebrow">Manufacturing Intelligence</span>
                <h3>Code Drift & Revision Analytics</h3>
            </div>
            <StatusBadge variant="brand">Automated Metric Engine</StatusBadge>
        </div>

        <div class="stat-grid">
            {#each analyticsKPIs as kpi}
                <div class="stat-card">
                    <span class="stat-label">{kpi.label}</span>
                    <span class="stat-value">{kpi.value}</span>
                    <span class="stat-sub">{kpi.sub}</span>
                </div>
            {/each}
        </div>
    </div>

    <div class="two-col">
        <!-- File Format Breakdown -->
        <div class="card">
            <div class="card-header">
                <h3><FileCode size={18} /> Program Format Distribution</h3>
            </div>
            <div class="format-list">
                {#each fileFormatDistribution as fmt}
                    <div class="format-row">
                        <div class="fmt-top">
                            <span class="fmt-name">{fmt.format}</span>
                            <span class="fmt-meta">{fmt.count} files ({fmt.percentage}) · {fmt.size}</span>
                        </div>
                        <div class="bar-track">
                            <div class="bar-fill" style="width: {fmt.percentage}; background: {fmt.color}"></div>
                        </div>
                    </div>
                {/each}
            </div>
        </div>

        <!-- Compliance & Integrity Scorecard -->
        <div class="card">
            <div class="card-header">
                <h3><ShieldCheck size={18} /> Compliance & Security Scorecard</h3>
            </div>
            <div class="scorecard">
                <div class="score-box">
                    <span class="score-num">100%</span>
                    <span class="score-text">SHA-256 Hash Verification Rate</span>
                </div>
                <div class="check-list">
                    <div class="check-item">
                        <CheckCircle2 size={16} class="c-icon success" />
                        <span>All stored file binaries match target checksums</span>
                    </div>
                    <div class="check-item">
                        <CheckCircle2 size={16} class="c-icon success" />
                        <span>100% Audit log traceability across all rollbacks</span>
                    </div>
                    <div class="check-item">
                        <CheckCircle2 size={16} class="c-icon success" />
                        <span>Role-Based Access Control (RBAC) enforced</span>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Engineering Upload Heatmap -->
    <div class="card">
        <div class="card-header">
            <h3><Calendar size={18} /> Engineering Upload Heatmap (Peak Hours)</h3>
            <span class="card-action">Shift Distribution</span>
        </div>
        <div class="table-container">
            <table class="heatmap-table">
                <thead>
                    <tr>
                        <th>Day</th>
                        <th>Morning Shift (08:00 - 12:00)</th>
                        <th>Afternoon Shift (12:00 - 16:00)</th>
                        <th>Evening Shift (16:00 - 20:00)</th>
                    </tr>
                </thead>
                <tbody>
                    {#each weeklyHeatmap as row}
                        <tr>
                            <td class="day-col">{row.day}</td>
                            <td><div class="heat-pill" style="opacity: {Math.max(0.3, row.h08_12 / 45)}">{row.h08_12} uploads</div></td>
                            <td><div class="heat-pill peak" style="opacity: {Math.max(0.4, row.h12_16 / 45)}">{row.h12_16} uploads</div></td>
                            <td><div class="heat-pill" style="opacity: {Math.max(0.3, row.h16_20 / 45)}">{row.h16_20} uploads</div></td>
                        </tr>
                    {/each}
                </tbody>
            </table>
        </div>
    </div>

    <!-- High-Revision Programs Watchlist -->
    <div class="card">
        <div class="card-header">
            <h3>Program Revision Intensity Matrix</h3>
        </div>
        <div class="table-container">
            <table class="data-table">
                <thead>
                    <tr>
                        <th>Program File</th>
                        <th>Assigned Machine</th>
                        <th>Revisions Depth</th>
                        <th>Risk Assessment</th>
                    </tr>
                </thead>
                <tbody>
                    {#each highChurnFiles as item}
                        <tr>
                            <td class="file-col">{item.file}</td>
                            <td class="meta-col">{item.machine}</td>
                            <td class="meta-col">{item.revisions} versions</td>
                            <td>
                                <StatusBadge variant={item.riskLevel === 'Attention' ? 'warning' : 'success'}>
                                    {item.riskLevel}
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
    .analytics-page {
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

    .card-header {
        display: flex;
        align-items: flex-start;
        justify-content: space-between;
        margin-bottom: var(--space-lg);
    }

    .card-header h3 {
        font-size: 18px;
        font-weight: 600;
        color: var(--color-ink);
        margin: 0;
        display: inline-flex;
        align-items: center;
        gap: var(--space-xs);
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
        font-size: 24px;
        font-weight: 700;
        color: var(--color-ink);
        letter-spacing: -0.5px;
    }

    .stat-sub {
        font-size: 12px;
        color: var(--color-ink-tertiary);
    }

    .two-col {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: var(--space-lg);
    }

    /* Formats */
    .format-list {
        display: flex;
        flex-direction: column;
        gap: var(--space-md);
    }

    .fmt-top {
        display: flex;
        justify-content: space-between;
        font-size: 13px;
        margin-bottom: 6px;
    }

    .fmt-name {
        font-weight: 600;
        color: var(--color-ink);
    }

    .fmt-meta {
        color: var(--color-ink-subtle);
    }

    .bar-track {
        height: 6px;
        background: var(--color-surface-2);
        border-radius: var(--radius-pill);
        overflow: hidden;
    }

    .bar-fill {
        height: 100%;
        border-radius: var(--radius-pill);
    }

    /* Scorecard */
    .scorecard {
        display: flex;
        flex-direction: column;
        gap: var(--space-md);
    }

    .score-box {
        display: flex;
        align-items: center;
        gap: var(--space-md);
        padding: var(--space-md);
        background: rgba(39, 166, 68, 0.08);
        border: 1px solid rgba(39, 166, 68, 0.2);
        border-radius: var(--radius-md);
    }

    .score-num {
        font-size: 32px;
        font-weight: 800;
        color: var(--color-success);
    }

    .score-text {
        font-size: 14px;
        font-weight: 600;
        color: var(--color-ink);
    }

    .check-list {
        display: flex;
        flex-direction: column;
        gap: var(--space-xs);
    }

    .check-item {
        display: flex;
        align-items: center;
        gap: var(--space-xs);
        font-size: 13px;
        color: var(--color-ink-muted);
    }

    .check-item :global(.c-icon.success) {
        color: var(--color-success);
        flex-shrink: 0;
    }

    /* Heatmap Table */
    .heatmap-table {
        width: 100%;
        border-collapse: collapse;
    }

    .heatmap-table th {
        text-align: left;
        font-size: 12px;
        font-weight: 600;
        color: var(--color-ink-tertiary);
        padding: var(--space-xs) var(--space-sm);
        border-bottom: 1px solid var(--color-hairline);
    }

    .heatmap-table td {
        padding: var(--space-xs) var(--space-sm);
        border-bottom: 1px solid var(--color-hairline);
    }

    .day-col {
        font-weight: 600;
        font-size: 13px;
        color: var(--color-ink);
    }

    .heat-pill {
        background: var(--color-primary);
        color: #ffffff;
        padding: 6px 12px;
        border-radius: var(--radius-md);
        font-size: 12px;
        font-weight: 600;
        text-align: center;
    }

    .heat-pill.peak {
        background: var(--color-primary-hover);
    }

    /* Data Table */
    .table-container { overflow-x: auto; }
    .data-table { width: 100%; border-collapse: collapse; }
    .data-table th { text-align: left; font-size: 12px; font-weight: 600; color: var(--color-ink-tertiary); padding: var(--space-sm); border-bottom: 1px solid var(--color-hairline); }
    .data-table td { padding: var(--space-sm); border-bottom: 1px solid var(--color-hairline); font-size: 13px; }
    .file-col { font-family: var(--font-mono); font-weight: 600; color: var(--color-ink); }
    .meta-col { color: var(--color-ink-subtle); }

    @media (max-width: 768px) {
        .two-col { grid-template-columns: 1fr; }
    }
</style>
