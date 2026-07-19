<script lang="ts">
    import { user } from '../authStore';
    import StatusBadge from '../components/StatusBadge.svelte';
    import EmptyState from '../components/EmptyState.svelte';
    import { Search, FileText, Download, Eye, X, Clock, Hash } from '@lucide/svelte';

    export let showToast: (msg: string, type: 'success' | 'error' | 'warning' | 'info') => void = () => {};

    const API_BASE_URL = 'http://localhost:5000';

    let viewMachineId = '';
    let files: any[] = [];
    let selectedFile: any = null;
    let drawerOpen = false;

    async function fetchFiles() {
        if (!viewMachineId) return;
        try {
            const response = await fetch(`${API_BASE_URL}/files/${viewMachineId}`);
            const data = await response.json();
            if (response.ok) {
                files = data.files;
                if (files.length === 0) {
                    showToast('No files found for this machine', 'info');
                }
            } else {
                files = [];
                showToast(data.message || 'No files found', 'error');
            }
        } catch (e) {
            showToast('Network error', 'error');
        }
    }

    function openDrawer(file: any) {
        selectedFile = file;
        drawerOpen = true;
    }

    function closeDrawer() {
        drawerOpen = false;
        selectedFile = null;
    }

    async function downloadFile(file: any) {
        try {
            const response = await fetch(`${API_BASE_URL}/download`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    machine_id: Number(viewMachineId),
                    file_name: file.file_name,
                    version_no: file.version_no,
                    user_id: $user?.id
                }),
            });
            if (response.ok) {
                const blob = await response.blob();
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = file.file_name;
                a.click();
                window.URL.revokeObjectURL(url);
                showToast(`Downloaded ${file.file_name}`, 'success');
            } else {
                showToast('Download failed', 'error');
            }
        } catch {
            showToast('Network error', 'error');
        }
    }

    // Group files by file_name to show version history
    $: groupedFiles = files.reduce((groups: Record<string, any[]>, file: any) => {
        if (!groups[file.file_name]) groups[file.file_name] = [];
        groups[file.file_name].push(file);
        return groups;
    }, {});
</script>

<div class="files-page">
    <div class="card">
        <div class="card-header">
            <h3>File Browser</h3>
        </div>

        <div class="search-row">
            <div class="search-input">
                <Search size={16} />
                <input
                    type="number"
                    bind:value={viewMachineId}
                    placeholder="Enter Machine ID"
                    on:keydown={(e) => e.key === 'Enter' && fetchFiles()}
                />
            </div>
            <button class="primary-btn" on:click={fetchFiles}>
                <Search size={14} /> Search
            </button>
        </div>

        {#if files.length > 0}
            <div class="table-container">
                <table class="data-table">
                    <thead>
                        <tr>
                            <th>File Name</th>
                            <th>Version</th>
                            <th>Date</th>
                            <th>Uploaded By</th>
                            <th></th>
                        </tr>
                    </thead>
                    <tbody>
                        {#each files as file}
                            <tr on:click={() => openDrawer(file)} class="clickable">
                                <td>
                                    <div class="file-cell">
                                        <FileText size={16} />
                                        <span class="file-name-text">{file.file_name}</span>
                                    </div>
                                </td>
                                <td>
                                    <StatusBadge variant="brand">v{file.version_no}</StatusBadge>
                                </td>
                                <td class="meta-text">{new Date(file.created_at || file.upload_time).toLocaleDateString()}</td>
                                <td class="meta-text">{file.uploaded_by}</td>
                                <td>
                                    {#if $user?.role === 'admin'}
                                        <button class="icon-btn" on:click|stopPropagation={() => downloadFile(file)} title="Download">
                                            <Download size={14} />
                                        </button>
                                    {/if}
                                </td>
                            </tr>
                        {/each}
                    </tbody>
                </table>
            </div>
        {:else}
            <EmptyState
                icon={FileText}
                title="No files to display"
                description="Search by Machine ID to see program files and their version history."
            />
        {/if}
    </div>
</div>

<!-- File Detail Drawer -->
{#if drawerOpen && selectedFile}
    <div class="drawer-overlay" on:click={closeDrawer}>
        <div class="drawer" on:click|stopPropagation>
            <div class="drawer-header">
                <h3>{selectedFile.file_name}</h3>
                <button class="icon-btn" on:click={closeDrawer}>
                    <X size={18} />
                </button>
            </div>

            <div class="drawer-body">
                <div class="detail-row">
                    <Clock size={14} />
                    <span class="detail-label">Uploaded</span>
                    <span class="detail-value">{new Date(selectedFile.created_at || selectedFile.upload_time).toLocaleString()}</span>
                </div>
                <div class="detail-row">
                    <Hash size={14} />
                    <span class="detail-label">Version</span>
                    <StatusBadge variant="brand">v{selectedFile.version_no}</StatusBadge>
                </div>
                {#if selectedFile.file_hash}
                    <div class="detail-row">
                        <Hash size={14} />
                        <span class="detail-label">SHA256</span>
                        <code class="hash-value">{selectedFile.file_hash?.slice(0, 16)}...</code>
                    </div>
                {/if}

                <div class="drawer-section">
                    <h4>Version History</h4>
                    {#if groupedFiles[selectedFile.file_name]}
                        <div class="version-timeline">
                            {#each groupedFiles[selectedFile.file_name].sort((a, b) => b.version_no - a.version_no) as ver}
                                <div class="version-item" class:current={ver.version_no === selectedFile.version_no}>
                                    <span class="version-dot"></span>
                                    <div class="version-info">
                                        <span class="version-label">Version {ver.version_no}</span>
                                        <span class="version-meta">{new Date(ver.created_at || ver.upload_time).toLocaleDateString()}</span>
                                    </div>
                                    {#if $user?.role === 'admin'}
                                        <button class="icon-btn" on:click={() => downloadFile(ver)} title="Download v{ver.version_no}">
                                            <Download size={14} />
                                        </button>
                                    {/if}
                                </div>
                            {/each}
                        </div>
                    {/if}
                </div>
            </div>
        </div>
    </div>
{/if}

<style>
    .files-page {
        max-width: 960px;
    }

    .card {
        background: var(--color-surface-1);
        border: 1px solid var(--color-hairline);
        border-radius: var(--radius-lg);
        padding: var(--space-lg);
    }

    .card-header {
        margin-bottom: var(--space-lg);
    }

    .card-header h3 {
        font-size: 18px;
        font-weight: 600;
        color: var(--color-ink);
        margin: 0;
    }

    .search-row {
        display: flex;
        gap: var(--space-sm);
        margin-bottom: var(--space-lg);
    }

    .search-input {
        display: flex;
        align-items: center;
        gap: var(--space-xs);
        padding: 0 var(--space-sm);
        background: var(--color-surface-2);
        border: 1px solid var(--color-hairline);
        border-radius: var(--radius-md);
        color: var(--color-ink-subtle);
        flex: 1;
        max-width: 240px;
    }

    .search-input input {
        border: none;
        background: transparent;
        padding: 8px 0;
        width: 100%;
        font-size: 14px;
    }

    .search-input input:focus {
        box-shadow: none;
    }

    .primary-btn {
        padding: 8px 16px;
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

    .primary-btn:hover {
        background: var(--color-primary-hover);
    }

    /* Table */
    .table-container {
        overflow-x: auto;
    }

    .data-table {
        width: 100%;
        border-collapse: collapse;
    }

    .data-table th {
        text-align: left;
        font-size: 12px;
        font-weight: 600;
        color: var(--color-ink-tertiary);
        text-transform: uppercase;
        letter-spacing: 0.04em;
        padding: var(--space-sm) var(--space-sm);
        border-bottom: 1px solid var(--color-hairline);
    }

    .data-table td {
        padding: var(--space-sm);
        border-bottom: 1px solid var(--color-hairline);
        font-size: 14px;
        color: var(--color-ink-muted);
    }

    .data-table tr.clickable {
        cursor: pointer;
        transition: background var(--transition-fast);
    }

    .data-table tr.clickable:hover {
        background: var(--color-surface-2);
    }

    .file-cell {
        display: flex;
        align-items: center;
        gap: var(--space-xs);
        color: var(--color-ink);
        font-weight: 500;
    }

    .file-cell :global(svg) {
        color: var(--color-ink-subtle);
        flex-shrink: 0;
    }

    .meta-text {
        color: var(--color-ink-subtle);
    }

    .icon-btn {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 28px;
        height: 28px;
        border: 1px solid var(--color-hairline);
        background: transparent;
        color: var(--color-ink-subtle);
        border-radius: var(--radius-sm);
        cursor: pointer;
        transition: all var(--transition-fast);
    }

    .icon-btn:hover {
        background: var(--color-surface-2);
        color: var(--color-ink);
        border-color: var(--color-hairline-strong);
    }

    /* Drawer */
    .drawer-overlay {
        position: fixed;
        inset: 0;
        background: var(--color-overlay);
        z-index: 1000;
        display: flex;
        justify-content: flex-end;
        animation: fadeIn 150ms ease;
    }

    .drawer {
        width: 100%;
        max-width: 420px;
        background: var(--color-surface-1);
        border-left: 1px solid var(--color-hairline);
        height: 100%;
        overflow-y: auto;
        animation: slideIn 250ms cubic-bezier(0.34, 1.56, 0.64, 1);
    }

    .drawer-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: var(--space-lg);
        border-bottom: 1px solid var(--color-hairline);
    }

    .drawer-header h3 {
        font-size: 16px;
        font-weight: 600;
        color: var(--color-ink);
        margin: 0;
        font-family: var(--font-mono);
    }

    .drawer-body {
        padding: var(--space-lg);
        display: flex;
        flex-direction: column;
        gap: var(--space-md);
    }

    .detail-row {
        display: flex;
        align-items: center;
        gap: var(--space-sm);
        font-size: 13px;
    }

    .detail-row :global(svg) {
        color: var(--color-ink-tertiary);
        flex-shrink: 0;
    }

    .detail-label {
        color: var(--color-ink-subtle);
        min-width: 70px;
    }

    .detail-value {
        color: var(--color-ink-muted);
    }

    .hash-value {
        font-family: var(--font-mono);
        font-size: 12px;
        background: var(--color-surface-2);
        padding: 2px 8px;
        border-radius: var(--radius-sm);
        color: var(--color-ink-subtle);
    }

    .drawer-section {
        margin-top: var(--space-md);
    }

    .drawer-section h4 {
        font-size: 13px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        color: var(--color-ink-subtle);
        margin-bottom: var(--space-md);
    }

    .version-timeline {
        display: flex;
        flex-direction: column;
        gap: var(--space-sm);
    }

    .version-item {
        display: flex;
        align-items: center;
        gap: var(--space-sm);
        padding: var(--space-xs) var(--space-sm);
        border-radius: var(--radius-md);
        transition: background var(--transition-fast);
    }

    .version-item:hover {
        background: var(--color-surface-2);
    }

    .version-item.current {
        background: rgba(94, 106, 210, 0.08);
        border: 1px solid rgba(94, 106, 210, 0.2);
    }

    .version-dot {
        width: 8px;
        height: 8px;
        border-radius: var(--radius-full);
        background: var(--color-ink-tertiary);
        flex-shrink: 0;
    }

    .version-item.current .version-dot {
        background: var(--color-primary);
    }

    .version-info {
        flex: 1;
        display: flex;
        flex-direction: column;
    }

    .version-label {
        font-size: 14px;
        font-weight: 500;
        color: var(--color-ink);
    }

    .version-meta {
        font-size: 12px;
        color: var(--color-ink-tertiary);
    }

    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }

    @keyframes slideIn {
        from { transform: translateX(100%); }
        to { transform: translateX(0); }
    }
</style>
