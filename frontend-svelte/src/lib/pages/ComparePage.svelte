<script lang="ts">
    import { user } from '../authStore';
    import { ArrowLeftRight } from '@lucide/svelte';

    export let showToast: (msg: string, type: 'success' | 'error' | 'warning' | 'info') => void = () => {};

    import { apiFetch } from '../api';

    let machineId = '';
    let fileName = '';
    let versionA = '';
    let versionB = '';
    let diffLines: string[] = [];
    let loading = false;

    async function handleCompare() {
        if (!machineId || !fileName || !versionA || !versionB) {
            showToast('Please fill in all fields', 'error');
            return;
        }
        loading = true;
        try {
            const response = await apiFetch('/diff', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    machine_id: Number(machineId),
                    file_name: fileName,
                    version_a: Number(versionA),
                    version_b: Number(versionB),
                    user_id: $user?.id,
                }),
            });
            const data = await response.json();
            if (response.ok && (data.status === 'Success' || data.status === 'success')) {
                diffLines = data.diff;
                showToast('Comparison generated', 'success');
            } else {
                showToast(data.message || 'Comparison failed', 'error');
            }
        } catch {
            showToast('Network error', 'error');
        } finally {
            loading = false;
        }
    }

    function getLineClass(line: string): string {
        if (line.startsWith('+')) return 'added';
        if (line.startsWith('-')) return 'removed';
        return '';
    }
</script>

<div class="compare-page">
    <div class="card">
        <div class="card-header">
            <h3>Compare Versions</h3>
        </div>

        <form on:submit|preventDefault={handleCompare}>
            <div class="form-grid">
                <div class="form-group">
                    <label>Machine ID</label>
                    <input type="number" bind:value={machineId} placeholder="e.g. 101" required />
                </div>
                <div class="form-group">
                    <label>File Name</label>
                    <input type="text" bind:value={fileName} placeholder="e.g. pump_housing.nc" required />
                </div>
                <div class="form-group">
                    <label>Version A</label>
                    <input type="number" bind:value={versionA} placeholder="e.g. 1" required />
                </div>
                <div class="form-group">
                    <label>Version B</label>
                    <input type="number" bind:value={versionB} placeholder="e.g. 2" required />
                </div>
            </div>

            <button type="submit" class="primary-btn" disabled={loading}>
                <ArrowLeftRight size={14} />
                {loading ? 'Comparing...' : 'Generate Diff'}
            </button>
        </form>
    </div>

    {#if diffLines.length > 0}
        <div class="diff-card">
            <div class="diff-header">
                <span class="diff-title">Diff: v{versionA} → v{versionB}</span>
                <span class="diff-meta">{diffLines.length} lines</span>
            </div>
            <div class="diff-body">
                {#each diffLines as line, i}
                    <div class="diff-line {getLineClass(line)}">
                        <span class="line-num">{i + 1}</span>
                        <span class="line-indicator">
                            {#if line.startsWith('+')}+{:else if line.startsWith('-')}−{:else}&nbsp;{/if}
                        </span>
                        <pre class="line-content">{line.slice(1) || line}</pre>
                    </div>
                {/each}
            </div>
        </div>
    {/if}
</div>

<style>
    .compare-page {
        display: flex;
        flex-direction: column;
        gap: var(--space-lg);
        max-width: 900px;
    }

    .card {
        background: var(--color-surface-1);
        border: 1px solid var(--color-hairline);
        border-radius: var(--radius-lg);
        padding: var(--space-lg);
    }

    .card-header { margin-bottom: var(--space-lg); }
    .card-header h3 { font-size: 18px; font-weight: 600; color: var(--color-ink); margin: 0; }

    .form-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: var(--space-md);
        margin-bottom: var(--space-lg);
    }

    .form-group label {
        display: block;
        font-size: 13px;
        font-weight: 500;
        color: var(--color-ink-subtle);
        margin-bottom: var(--space-xs);
    }

    .primary-btn {
        padding: 10px 20px;
        background: var(--color-primary);
        color: var(--color-on-primary);
        border: none;
        border-radius: var(--radius-md);
        font-size: 14px;
        font-weight: 500;
        cursor: pointer;
        display: inline-flex;
        align-items: center;
        gap: var(--space-xs);
        transition: background var(--transition-fast);
    }

    .primary-btn:hover { background: var(--color-primary-hover); }
    .primary-btn:disabled { opacity: 0.5; cursor: not-allowed; }

    /* Diff Viewer */
    .diff-card {
        background: var(--color-surface-1);
        border: 1px solid var(--color-hairline);
        border-radius: var(--radius-lg);
        overflow: hidden;
    }

    .diff-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: var(--space-sm) var(--space-md);
        border-bottom: 1px solid var(--color-hairline);
        background: var(--color-surface-2);
    }

    .diff-title {
        font-size: 13px;
        font-weight: 600;
        color: var(--color-ink-muted);
        font-family: var(--font-mono);
    }

    .diff-meta {
        font-size: 12px;
        color: var(--color-ink-tertiary);
    }

    .diff-body {
        overflow-x: auto;
        font-family: var(--font-mono);
        font-size: 13px;
    }

    .diff-line {
        display: flex;
        align-items: stretch;
        min-height: 24px;
        border-bottom: 1px solid var(--color-hairline);
    }

    .diff-line:last-child {
        border-bottom: none;
    }

    .line-num {
        width: 48px;
        flex-shrink: 0;
        padding: 2px var(--space-sm);
        text-align: right;
        color: var(--color-ink-tertiary);
        font-size: 12px;
        user-select: none;
        border-right: 1px solid var(--color-hairline);
    }

    .line-indicator {
        width: 24px;
        flex-shrink: 0;
        text-align: center;
        padding: 2px 0;
        font-weight: 600;
        user-select: none;
    }

    .line-content {
        flex: 1;
        padding: 2px var(--space-sm);
        white-space: pre;
        margin: 0;
        font: inherit;
    }

    .diff-line.added {
        background: var(--color-success-subtle);
    }
    .diff-line.added .line-indicator {
        color: var(--color-success);
    }

    .diff-line.removed {
        background: var(--color-error-subtle);
    }
    .diff-line.removed .line-indicator {
        color: var(--color-error);
    }

    @media (max-width: 640px) {
        .form-grid { grid-template-columns: 1fr; }
    }
</style>
