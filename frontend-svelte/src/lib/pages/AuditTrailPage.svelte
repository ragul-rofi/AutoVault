<script lang="ts">
    import StatusBadge from '../components/StatusBadge.svelte';
    import { Upload, RotateCcw, Download, ArrowLeftRight, Filter } from '@lucide/svelte';

    const auditLogs = [
        { id: 1, action: 'UPLOAD', user: 'Jane Smith', machine: 'Machine 102', file: 'turbine_blade.nc', version: 3, timestamp: '2026-07-19T09:42:00', detail: 'New version uploaded' },
        { id: 2, action: 'ROLLBACK', user: 'John Doe', machine: 'Machine 101', file: 'pump_housing.nc', version: 1, timestamp: '2026-07-19T08:15:00', detail: 'Rolled back to v1' },
        { id: 3, action: 'DOWNLOAD', user: 'Bob Johnson', machine: 'Machine 103', file: 'valve_seal.gcode', version: 2, timestamp: '2026-07-18T16:10:00', detail: 'Downloaded v2' },
        { id: 4, action: 'DIFF', user: 'John Doe', machine: 'Machine 102', file: 'turbine_blade.nc', version: 3, timestamp: '2026-07-18T14:05:00', detail: 'Compared v2 vs v3' },
        { id: 5, action: 'UPLOAD', user: 'Jane Smith', machine: 'Machine 101', file: 'pump_housing.nc', version: 2, timestamp: '2026-07-17T11:30:00', detail: 'Feedrate optimized version' },
    ];

    let filterAction = '';

    $: filteredLogs = filterAction
        ? auditLogs.filter(l => l.action === filterAction)
        : auditLogs;

    function actionIcon(action: string) {
        switch (action) {
            case 'UPLOAD': return Upload;
            case 'ROLLBACK': return RotateCcw;
            case 'DOWNLOAD': return Download;
            case 'DIFF': return ArrowLeftRight;
            default: return Upload;
        }
    }

    function actionVariant(action: string): 'success' | 'warning' | 'info' | 'brand' {
        switch (action) {
            case 'UPLOAD': return 'success';
            case 'ROLLBACK': return 'warning';
            case 'DOWNLOAD': return 'info';
            case 'DIFF': return 'brand';
            default: return 'info';
        }
    }

    function formatDate(ts: string): string {
        return new Date(ts).toLocaleString();
    }
</script>

<div class="audit-page">
    <div class="card">
        <div class="card-header">
            <h3>Audit Trail</h3>
            <div class="filter-row">
                <Filter size={14} />
                <select bind:value={filterAction}>
                    <option value="">All actions</option>
                    <option value="UPLOAD">Upload</option>
                    <option value="ROLLBACK">Rollback</option>
                    <option value="DOWNLOAD">Download</option>
                    <option value="DIFF">Diff</option>
                </select>
            </div>
        </div>

        <div class="audit-list">
            {#each filteredLogs as log}
                <div class="audit-entry">
                    <div class="audit-icon">
                        <svelte:component this={actionIcon(log.action)} size={16} />
                    </div>
                    <div class="audit-content">
                        <div class="audit-top">
                            <span class="audit-user">{log.user}</span>
                            <StatusBadge variant={actionVariant(log.action)}>{log.action}</StatusBadge>
                        </div>
                        <p class="audit-detail">{log.detail}</p>
                        <div class="audit-meta">
                            <span class="audit-file">{log.file} v{log.version}</span>
                            <span>·</span>
                            <span>{log.machine}</span>
                            <span>·</span>
                            <span>{formatDate(log.timestamp)}</span>
                        </div>
                    </div>
                </div>
            {/each}
        </div>
    </div>
</div>

<style>
    .audit-page { max-width: 800px; }

    .card {
        background: var(--color-surface-1);
        border: 1px solid var(--color-hairline);
        border-radius: var(--radius-lg);
        padding: var(--space-lg);
    }

    .card-header {
        display: flex; justify-content: space-between; align-items: center;
        margin-bottom: var(--space-lg);
    }
    .card-header h3 { font-size: 18px; font-weight: 600; color: var(--color-ink); margin: 0; }

    .filter-row {
        display: flex;
        align-items: center;
        gap: var(--space-xs);
        color: var(--color-ink-subtle);
    }

    .filter-row select {
        max-width: 160px;
        font-size: 13px;
        padding: 6px 10px;
    }

    .audit-list {
        display: flex;
        flex-direction: column;
        gap: var(--space-sm);
    }

    .audit-entry {
        display: flex;
        gap: var(--space-sm);
        padding: var(--space-sm) var(--space-md);
        border: 1px solid var(--color-hairline);
        border-radius: var(--radius-md);
        transition: border-color var(--transition-fast);
    }

    .audit-entry:hover {
        border-color: var(--color-hairline-strong);
    }

    .audit-icon {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 32px;
        height: 32px;
        background: var(--color-surface-2);
        border-radius: var(--radius-md);
        color: var(--color-ink-subtle);
        flex-shrink: 0;
        margin-top: 2px;
    }

    .audit-content {
        flex: 1;
        min-width: 0;
    }

    .audit-top {
        display: flex;
        align-items: center;
        gap: var(--space-xs);
        margin-bottom: 2px;
    }

    .audit-user {
        font-size: 14px;
        font-weight: 600;
        color: var(--color-ink);
    }

    .audit-detail {
        font-size: 13px;
        color: var(--color-ink-muted);
        margin: 0;
    }

    .audit-meta {
        display: flex;
        gap: var(--space-xs);
        font-size: 12px;
        color: var(--color-ink-tertiary);
        margin-top: 4px;
        flex-wrap: wrap;
    }

    .audit-file {
        font-family: var(--font-mono);
    }
</style>
