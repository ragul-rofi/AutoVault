<script lang="ts">
    import { user } from '../authStore';
    import { RotateCcw, AlertTriangle } from '@lucide/svelte';

    export let showToast: (msg: string, type: 'success' | 'error' | 'warning' | 'info') => void = () => {};

    import { API_BASE_URL } from '../config';

    let machineId = '';
    let fileName = '';
    let targetVersion = '';
    let loading = false;

    async function handleRollback() {
        if (!machineId || !fileName || !targetVersion) {
            showToast('Please fill in all fields', 'error');
            return;
        }
        loading = true;
        try {
            const response = await fetch(`${API_BASE_URL}/rollback`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    machine_id: Number(machineId),
                    file_name: fileName,
                    target_version: Number(targetVersion),
                    uploaded_by: $user?.id,
                }),
            });
            const data = await response.json();
            if (response.ok) {
                showToast(data.message || 'Rollback successful', 'success');
                machineId = ''; fileName = ''; targetVersion = '';
            } else {
                showToast(data.message || 'Rollback failed', 'error');
            }
        } catch {
            showToast('Network error', 'error');
        } finally {
            loading = false;
        }
    }
</script>

<div class="rollback-page">
    <div class="card">
        <div class="card-header">
            <h3>Rollback File Version</h3>
        </div>

        <div class="warning-banner">
            <AlertTriangle size={16} />
            <span>Rollback will create a new version pointing to the target version's content. This action is logged.</span>
        </div>

        <form on:submit|preventDefault={handleRollback}>
            <div class="form-grid">
                <div class="form-group">
                    <label for="rb-machine">Machine ID</label>
                    <input id="rb-machine" type="number" bind:value={machineId} placeholder="e.g. 101" required />
                </div>
                <div class="form-group">
                    <label for="rb-file">File Name</label>
                    <input id="rb-file" type="text" bind:value={fileName} placeholder="e.g. pump_housing.nc" required />
                </div>
                <div class="form-group">
                    <label for="rb-version">Target Version</label>
                    <input id="rb-version" type="number" bind:value={targetVersion} placeholder="e.g. 1" required />
                </div>
            </div>

            <button type="submit" class="primary-btn" disabled={loading}>
                <RotateCcw size={14} />
                {loading ? 'Rolling back...' : 'Perform Rollback'}
            </button>
        </form>
    </div>
</div>

<style>
    .rollback-page { max-width: 600px; }

    .card {
        background: var(--color-surface-1);
        border: 1px solid var(--color-hairline);
        border-radius: var(--radius-lg);
        padding: var(--space-lg);
    }

    .card-header { margin-bottom: var(--space-lg); }
    .card-header h3 { font-size: 18px; font-weight: 600; color: var(--color-ink); margin: 0; }

    .warning-banner {
        display: flex;
        align-items: flex-start;
        gap: var(--space-sm);
        padding: var(--space-sm) var(--space-md);
        background: var(--color-warning-subtle);
        border: 1px solid rgba(245, 158, 11, 0.2);
        border-radius: var(--radius-md);
        font-size: 13px;
        color: var(--color-warning);
        margin-bottom: var(--space-lg);
        line-height: 1.5;
    }

    .warning-banner :global(svg) { flex-shrink: 0; margin-top: 1px; }

    .form-grid {
        display: grid;
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
</style>
