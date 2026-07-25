<script lang="ts">
    import { onMount } from 'svelte';
    import { user } from '../authStore';
    import StatusBadge from '../components/StatusBadge.svelte';
    import EmptyState from '../components/EmptyState.svelte';
    import Modal from '../components/Modal.svelte';
    import { Search, FileText, Download, Eye, X, Clock, Hash, Cpu, Edit3, Code, Save, Check } from '@lucide/svelte';
    import { apiFetch } from '../api';

    export let showToast: (msg: string, type: 'success' | 'error' | 'warning' | 'info') => void = () => {};
    export let targetFile: any = null;

    let viewMachineId = '101';
    let files: any[] = [];
    let selectedFile: any = null;
    let drawerOpen = false;

    // View & Edit Modal States
    let viewModalOpen = false;
    let editModalOpen = false;
    let viewingContent = '';
    let editingContent = '';
    let viewingFileName = '';
    let viewingVersion = 1;
    let viewingMachineId = 101;
    let loadingContent = false;
    let savingEdit = false;

    onMount(() => {
        if (targetFile) {
            if (targetFile.machine_id) {
                viewMachineId = String(targetFile.machine_id);
            }
            openDrawer(targetFile);
        }
        fetchFiles();
    });

    $: if (targetFile) {
        if (targetFile.machine_id) {
            viewMachineId = String(targetFile.machine_id);
        }
        openDrawer(targetFile);
    }

    async function fetchFiles() {
        if (!viewMachineId) return;
        try {
            const response = await apiFetch(`/files/${viewMachineId}`);
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
            if (viewMachineId === '101') {
                files = [
                    { file_name: 'pump_housing.nc', machine_id: 101, version_no: 2, uploaded_by: 'John Doe', upload_time: '2026-07-19T09:42:00', file_hash: 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855' },
                    { file_name: 'pump_housing.nc', machine_id: 101, version_no: 1, uploaded_by: 'John Doe', upload_time: '2026-07-18T14:30:00', file_hash: '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8' },
                    { file_name: 'bracket_arm.cnc', machine_id: 101, version_no: 4, uploaded_by: 'Jane Smith', upload_time: '2026-07-17T11:30:00', file_hash: '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8' },
                ];
            } else {
                files = [];
            }
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

    async function openViewModal(file: any) {
        viewingFileName = file.file_name;
        viewingVersion = file.version_no;
        viewingMachineId = Number(file.machine_id || viewMachineId);
        loadingContent = true;
        viewModalOpen = true;
        try {
            const res = await apiFetch(`/file-content?machine_id=${viewingMachineId}&file_name=${encodeURIComponent(viewingFileName)}&version_no=${viewingVersion}`);
            const data = await res.json();
            if (res.ok && data.status === 'success') {
                viewingContent = data.content || '';
            } else {
                viewingContent = `; Unable to load content (${data.message || 'Error'})`;
            }
        } catch {
            viewingContent = `; Offline mode - Sample G-Code for ${viewingFileName}\nG21 G90 G40 G80\nG28 G91 Z0\nM06 T01\nM03 S2000\nG00 X0 Y0\nG01 Z-5.0 F100\nM30`;
        } finally {
            loadingContent = false;
        }
    }

    async function openEditModal(file: any) {
        viewingFileName = file.file_name;
        viewingVersion = file.version_no;
        viewingMachineId = Number(file.machine_id || viewMachineId);
        loadingContent = true;
        editModalOpen = true;
        try {
            const res = await apiFetch(`/file-content?machine_id=${viewingMachineId}&file_name=${encodeURIComponent(viewingFileName)}&version_no=${viewingVersion}`);
            const data = await res.json();
            if (res.ok && data.status === 'success') {
                editingContent = data.content || '';
            } else {
                editingContent = `% \n(NEW REVISION FOR ${viewingFileName})\nG21 G90 G40 G80\nM30\n%`;
            }
        } catch {
            editingContent = `% \n(NEW REVISION FOR ${viewingFileName})\nG21 G90 G40 G80\nM30\n%`;
        } finally {
            loadingContent = false;
        }
    }

    async function handleSaveEdit() {
        if (!editingContent.trim()) {
            showToast('File content cannot be empty', 'error');
            return;
        }
        savingEdit = true;
        try {
            const res = await apiFetch('/files/save-content', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    machine_id: viewingMachineId,
                    file_name: viewingFileName,
                    content: editingContent,
                    uploaded_by: $user?.id || 1,
                }),
            });
            const data = await res.json();
            if (res.ok && data.status === 'success') {
                showToast(`Saved as Version v${data.version_no}`, 'success');
                editModalOpen = false;
                await fetchFiles();
            } else {
                showToast(data.message || 'Failed to save edit', 'error');
            }
        } catch {
            showToast('Network error while saving file', 'error');
        } finally {
            savingEdit = false;
        }
    }

    async function downloadFile(file: any) {
        try {
            const response = await apiFetch('/download', {
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
                showToast(`Downloaded mock ${file.file_name}`, 'success');
            }
        } catch {
            showToast(`Downloaded mock ${file.file_name}`, 'success');
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
                    placeholder="Enter Machine ID (101, 102, 103...)"
                    on:keydown={(e) => e.key === 'Enter' && fetchFiles()}
                />
            </div>
            <button class="primary-btn" on:click={fetchFiles}>
                <Search size={14} /> Search Machine
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
                            <th>Action</th>
                        </tr>
                    </thead>
                    <tbody>
                        {#each files as file}
                            <tr on:click={() => openDrawer(file)} class="clickable" title="Click to view file preview and version history">
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
                                    <div class="action-cell">
                                        <button class="icon-btn" on:click|stopPropagation={() => openViewModal(file)} title="View Code Content">
                                            <Code size={14} />
                                        </button>
                                        {#if $user?.role === 'admin' || $user?.role === 'engineer'}
                                            <button class="icon-btn" on:click|stopPropagation={() => openEditModal(file)} title="Edit Program">
                                                <Edit3 size={14} />
                                            </button>
                                        {/if}
                                        <button class="icon-btn" on:click|stopPropagation={() => downloadFile(file)} title="Download">
                                            <Download size={14} />
                                        </button>
                                    </div>
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
                description="Search by Machine ID (e.g. 101, 102, 103) to see program files and their version history."
            />
        {/if}
    </div>
</div>

<!-- File Detail Drawer (Preview Page) -->
{#if drawerOpen && selectedFile}
    <div class="drawer-overlay" on:click={closeDrawer}>
        <div class="drawer" on:click|stopPropagation>
            <div class="drawer-header">
                <div class="drawer-title-group">
                    <FileText size={18} class="file-icon" />
                    <h3>{selectedFile.file_name}</h3>
                </div>
                <button class="icon-btn" on:click={closeDrawer}>
                    <X size={18} />
                </button>
            </div>

            <div class="drawer-body">
                <div class="detail-card">
                    <div class="detail-row">
                        <Cpu size={14} />
                        <span class="detail-label">Machine ID</span>
                        <span class="detail-value">Machine #{selectedFile.machine_id || viewMachineId}</span>
                    </div>
                    <div class="detail-row">
                        <Clock size={14} />
                        <span class="detail-label">Uploaded</span>
                        <span class="detail-value">{new Date(selectedFile.created_at || selectedFile.upload_time).toLocaleString()}</span>
                    </div>
                    <div class="detail-row">
                        <Hash size={14} />
                        <span class="detail-label">Active Version</span>
                        <StatusBadge variant="brand">v{selectedFile.version_no}</StatusBadge>
                    </div>
                    {#if selectedFile.file_hash}
                        <div class="detail-row">
                            <Hash size={14} />
                            <span class="detail-label">SHA256</span>
                            <code class="hash-value">{selectedFile.file_hash?.slice(0, 20)}...</code>
                        </div>
                    {/if}
                </div>

                <div class="drawer-actions-grid">
                    <button class="primary-btn" on:click={() => openViewModal(selectedFile)}>
                        <Code size={14} /> View Content
                    </button>
                    {#if $user?.role === 'admin' || $user?.role === 'engineer'}
                        <button class="secondary-btn" on:click={() => openEditModal(selectedFile)}>
                            <Edit3 size={14} /> Edit Program
                        </button>
                    {/if}
                    <button class="secondary-btn" on:click={() => downloadFile(selectedFile)}>
                        <Download size={14} /> Download
                    </button>
                </div>

                <div class="drawer-section">
                    <h4>Version Timeline & Revision History</h4>
                    {#if groupedFiles[selectedFile.file_name]}
                        <div class="version-timeline">
                            {#each groupedFiles[selectedFile.file_name].sort((a, b) => b.version_no - a.version_no) as ver}
                                <div class="version-item" class:current={ver.version_no === selectedFile.version_no}>
                                    <span class="version-dot"></span>
                                    <div class="version-info">
                                        <span class="version-label">Version {ver.version_no}</span>
                                        <span class="version-meta">{new Date(ver.created_at || ver.upload_time).toLocaleDateString()} · By {ver.uploaded_by}</span>
                                    </div>
                                    <div class="item-actions">
                                        <button class="icon-btn" on:click={() => openViewModal(ver)} title="View Code">
                                            <Code size={13} />
                                        </button>
                                        <button class="icon-btn" on:click={() => downloadFile(ver)} title="Download v{ver.version_no}">
                                            <Download size={13} />
                                        </button>
                                    </div>
                                </div>
                            {/each}
                        </div>
                    {/if}
                </div>
            </div>
        </div>
    </div>
{/if}

<!-- View Code Content Modal -->
<Modal open={viewModalOpen} title="Viewing Code: {viewingFileName} (v{viewingVersion})" on:close={() => viewModalOpen = false} size="lg">
    {#if loadingContent}
        <div class="modal-loading">Loading program file content...</div>
    {:else}
        <div class="code-viewer-container">
            <pre class="code-viewer">{viewingContent}</pre>
        </div>
    {/if}
</Modal>

<!-- Edit Code Content Modal -->
<Modal open={editModalOpen} title="Edit Program: {viewingFileName}" on:close={() => editModalOpen = false} size="lg">
    <div class="code-editor-modal">
        <p class="editor-subtitle">Modifying content will save as a new version <strong>v{viewingVersion + 1}</strong>.</p>
        <textarea class="code-editor-textarea" bind:value={editingContent} rows="14" placeholder="Enter G-code / NC program content..."></textarea>
        <div class="modal-actions-bar">
            <button class="secondary-btn" on:click={() => editModalOpen = false}>Cancel</button>
            <button class="primary-btn" on:click={handleSaveEdit} disabled={savingEdit}>
                <Save size={14} />
                {savingEdit ? 'Saving Version...' : 'Save as New Version'}
            </button>
        </div>
    </div>
</Modal>

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
        max-width: 320px;
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
        justify-content: center;
        gap: var(--space-xs);
        transition: background var(--transition-fast);
    }

    .primary-btn:hover {
        background: var(--color-primary-hover);
    }

    .primary-btn.full-width {
        width: 100%;
        padding: 10px;
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
        padding: var(--space-sm);
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
        color: var(--color-primary);
        flex-shrink: 0;
    }

    .action-cell {
        display: flex;
        gap: var(--space-xs);
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
        max-width: 440px;
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

    .drawer-title-group {
        display: flex;
        align-items: center;
        gap: var(--space-xs);
        color: var(--color-primary);
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
        gap: var(--space-lg);
    }

    .detail-card {
        background: var(--color-surface-2);
        border: 1px solid var(--color-hairline);
        border-radius: var(--radius-md);
        padding: var(--space-md);
        display: flex;
        flex-direction: column;
        gap: var(--space-sm);
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
        min-width: 100px;
    }

    .detail-value {
        color: var(--color-ink-muted);
        font-weight: 500;
    }

    .hash-value {
        font-family: var(--font-mono);
        font-size: 11px;
        background: var(--color-surface-3);
        padding: 2px 6px;
        border-radius: var(--radius-sm);
        color: var(--color-ink-subtle);
    }

    .drawer-actions {
        margin-top: -var(--space-xs);
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
        gap: var(--space-xs);
    }

    .version-item {
        display: flex;
        align-items: center;
        gap: var(--space-sm);
        padding: var(--space-xs) var(--space-sm);
        border-radius: var(--radius-md);
        background: var(--color-surface-2);
        border: 1px solid var(--color-hairline);
        transition: background var(--transition-fast);
    }

    .version-item:hover {
        border-color: var(--color-hairline-strong);
    }

    .version-item.current {
        background: rgba(94, 106, 210, 0.08);
        border: 1px solid rgba(94, 106, 210, 0.3);
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
        font-size: 13px;
        font-weight: 600;
        color: var(--color-ink);
    }

    .version-meta {
        font-size: 11px;
        color: var(--color-ink-tertiary);
    }

    .drawer-actions-grid {
        display: flex;
        gap: var(--space-xs);
        flex-wrap: wrap;
    }

    .drawer-actions-grid button {
        flex: 1;
        min-width: 110px;
        font-size: 12px;
        padding: 8px 12px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        gap: 6px;
    }

    .item-actions {
        display: flex;
        gap: 4px;
    }

    .secondary-btn {
        padding: 8px 16px;
        background: var(--color-surface-2);
        color: var(--color-ink);
        border: 1px solid var(--color-hairline);
        border-radius: var(--radius-md);
        font-size: 13px;
        font-weight: 500;
        cursor: pointer;
        display: inline-flex;
        align-items: center;
        gap: var(--space-xs);
        transition: all var(--transition-fast);
    }

    .secondary-btn:hover {
        background: var(--color-surface-3);
        border-color: var(--color-hairline-strong);
    }

    /* Modal Content Styles */
    .modal-loading {
        padding: var(--space-xl);
        text-align: center;
        color: var(--color-ink-subtle);
        font-size: 14px;
    }

    .code-viewer-container {
        max-height: 450px;
        overflow-y: auto;
        background: var(--color-surface-2);
        border: 1px solid var(--color-hairline);
        border-radius: var(--radius-md);
        padding: var(--space-md);
    }

    .code-viewer {
        margin: 0;
        font-family: var(--font-mono);
        font-size: 13px;
        color: var(--color-ink);
        white-space: pre-wrap;
        word-break: break-all;
        line-height: 1.6;
    }

    .code-editor-modal {
        display: flex;
        flex-direction: column;
        gap: var(--space-md);
    }

    .editor-subtitle {
        margin: 0;
        font-size: 13px;
        color: var(--color-ink-subtle);
    }

    .code-editor-textarea {
        width: 100%;
        box-sizing: border-box;
        font-family: var(--font-mono);
        font-size: 13px;
        line-height: 1.5;
        padding: var(--space-md);
        background: var(--color-surface-2);
        color: var(--color-ink);
        border: 1px solid var(--color-hairline);
        border-radius: var(--radius-md);
        resize: vertical;
        outline: none;
    }

    .code-editor-textarea:focus {
        border-color: var(--color-primary);
    }

    .modal-actions-bar {
        display: flex;
        justify-content: flex-end;
        gap: var(--space-sm);
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
