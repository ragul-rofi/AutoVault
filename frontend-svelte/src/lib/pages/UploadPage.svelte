<script lang="ts">
    import { user } from '../authStore';
    import { CloudUpload, File, CheckCircle, XCircle, RefreshCw, X, Trash2 } from '@lucide/svelte';

    export let showToast: (msg: string, type: 'success' | 'error' | 'warning' | 'info') => void = () => {};

    const API_BASE_URL = 'http://localhost:5000';

    let uploadMachineId = '';
    let dragActive = false;

    interface UploadedFile {
        id: string;
        name: string;
        size: number;
        type: string;
        progress: number;
        failed?: boolean;
        rawFile?: File;
    }

    let uploadedFiles: UploadedFile[] = [];

    function handleDragOver(event: DragEvent) {
        event.preventDefault();
        dragActive = true;
    }

    function handleDragLeave(event: DragEvent) {
        event.preventDefault();
        dragActive = false;
    }

    function handleDrop(event: DragEvent) {
        event.preventDefault();
        dragActive = false;
        if (event.dataTransfer?.files) {
            handleDropFiles(event.dataTransfer.files);
        }
    }

    function handleFileSelect(event: Event) {
        const input = event.target as HTMLInputElement;
        if (input.files) {
            handleDropFiles(input.files);
        }
    }

    function handleDropFiles(fileList: FileList) {
        if (!uploadMachineId) {
            showToast('Please enter a Machine ID first', 'error');
            return;
        }

        const newFiles = Array.from(fileList);
        const newFilesWithIds = newFiles.map((file) => ({
            id: Math.random().toString(36).slice(2),
            name: file.name,
            size: file.size,
            type: file.type,
            progress: 0,
            rawFile: file,
        }));

        uploadedFiles = [...newFilesWithIds, ...uploadedFiles];

        newFilesWithIds.forEach(({ id }, index) => {
            uploadFileWithProgress(newFiles[index], id);
        });
    }

    async function uploadFileWithProgress(file: File, id: string) {
        const formData = new FormData();
        formData.append('file', file);
        formData.append('machine_id', uploadMachineId);
        formData.append('uploaded_by', String($user?.id));

        try {
            let progress = 0;
            const interval = setInterval(() => {
                progress += 10;
                uploadedFiles = uploadedFiles.map((f) =>
                    f.id === id ? { ...f, progress: Math.min(progress, 90) } : f
                );
                if (progress >= 90) clearInterval(interval);
            }, 200);

            const response = await fetch(`${API_BASE_URL}/upload`, {
                method: 'POST',
                body: formData,
            });

            clearInterval(interval);
            const data = await response.json();

            if (response.ok) {
                uploadedFiles = uploadedFiles.map((f) =>
                    f.id === id ? { ...f, progress: 100 } : f
                );
                showToast(`${file.name} uploaded successfully`, 'success');
            } else {
                uploadedFiles = uploadedFiles.map((f) =>
                    f.id === id ? { ...f, failed: true, progress: 0 } : f
                );
                showToast(data.message || 'Upload failed', 'error');
            }
        } catch (e) {
            uploadedFiles = uploadedFiles.map((f) =>
                f.id === id ? { ...f, failed: true, progress: 0 } : f
            );
            showToast('Network error during upload', 'error');
        }
    }

    function deleteFile(id: string) {
        uploadedFiles = uploadedFiles.filter((f) => f.id !== id);
    }

    function retryFile(id: string) {
        const file = uploadedFiles.find((f) => f.id === id);
        if (file && file.rawFile) {
            uploadedFiles = uploadedFiles.map((f) =>
                f.id === id ? { ...f, failed: false, progress: 0 } : f
            );
            uploadFileWithProgress(file.rawFile, id);
        }
    }

    function getReadableFileSize(bytes: number): string {
        if (bytes === 0) return '0 B';
        const k = 1024;
        const sizes = ['B', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return Math.round((bytes / Math.pow(k, i)) * 100) / 100 + ' ' + sizes[i];
    }
</script>

<div class="upload-page">
    <div class="card">
        <div class="card-header">
            <h3>Upload Program Files</h3>
            <span class="card-hint">Drag & drop or browse</span>
        </div>

        <div class="form-row">
            <label for="machine-id">Machine ID</label>
            <input
                id="machine-id"
                type="number"
                bind:value={uploadMachineId}
                placeholder="e.g. 101"
                class="machine-input"
            />
        </div>

        <div
            class="dropzone"
            class:drag-active={dragActive}
            on:dragover={handleDragOver}
            on:dragleave={handleDragLeave}
            on:drop={handleDrop}
            role="button"
            tabindex="0"
        >
            <CloudUpload size={40} strokeWidth={1.25} />
            <p class="dropzone-title">Drop files here or click to browse</p>
            <p class="dropzone-hint">Supported: .nc, .cnc, .gcode</p>
            <input
                type="file"
                class="file-input-hidden"
                accept=".nc,.cnc,.gcode"
                on:change={handleFileSelect}
                multiple
            />
        </div>

        {#if uploadedFiles.length > 0}
            <div class="file-queue">
                {#each uploadedFiles as file (file.id)}
                    <div class="file-row" class:failed={file.failed}>
                        <div class="file-icon-wrap">
                            {#if file.progress === 100}
                                <CheckCircle size={18} />
                            {:else if file.failed}
                                <XCircle size={18} />
                            {:else}
                                <File size={18} />
                            {/if}
                        </div>
                        <div class="file-info">
                            <div class="file-name-row">
                                <span class="file-name">{file.name}</span>
                                <span class="file-size">{getReadableFileSize(file.size)}</span>
                            </div>
                            {#if !file.failed && file.progress < 100}
                                <div class="progress-track">
                                    <div class="progress-fill" style="width: {file.progress}%"></div>
                                </div>
                                <span class="progress-label">{file.progress}%</span>
                            {:else if file.failed}
                                <span class="error-label">Upload failed</span>
                            {/if}
                        </div>
                        <div class="file-actions">
                            {#if file.failed}
                                <button class="icon-btn" on:click={() => retryFile(file.id)} title="Retry">
                                    <RefreshCw size={14} />
                                </button>
                            {/if}
                            <button class="icon-btn" on:click={() => deleteFile(file.id)} title="Remove">
                                <X size={14} />
                            </button>
                        </div>
                    </div>
                {/each}
            </div>
        {/if}
    </div>
</div>

<style>
    .upload-page {
        max-width: 700px;
    }

    .card {
        background: var(--color-surface-1);
        border: 1px solid var(--color-hairline);
        border-radius: var(--radius-lg);
        padding: var(--space-lg);
    }

    .card-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: var(--space-lg);
    }

    .card-header h3 {
        font-size: 18px;
        font-weight: 600;
        color: var(--color-ink);
        margin: 0;
    }

    .card-hint {
        font-size: 12px;
        color: var(--color-ink-subtle);
        font-weight: 500;
    }

    .form-row {
        margin-bottom: var(--space-lg);
    }

    .form-row label {
        display: block;
        font-size: 13px;
        font-weight: 500;
        color: var(--color-ink-subtle);
        margin-bottom: var(--space-xs);
    }

    .machine-input {
        max-width: 200px;
    }

    /* Dropzone */
    .dropzone {
        position: relative;
        border: 2px dashed var(--color-hairline-strong);
        border-radius: var(--radius-lg);
        padding: var(--space-xxl) var(--space-lg);
        text-align: center;
        background: var(--color-canvas);
        cursor: pointer;
        transition: all var(--transition-base);
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: var(--space-xs);
        color: var(--color-ink-tertiary);
    }

    .dropzone:hover {
        border-color: var(--color-primary);
        background: rgba(94, 106, 210, 0.04);
    }

    .dropzone.drag-active {
        border-color: var(--color-primary);
        background: rgba(94, 106, 210, 0.08);
        transform: scale(1.01);
    }

    .dropzone-title {
        font-size: 15px;
        font-weight: 500;
        color: var(--color-ink-muted);
        margin: 0;
    }

    .dropzone-hint {
        font-size: 13px;
        color: var(--color-ink-tertiary);
        margin: 0;
    }

    .file-input-hidden {
        position: absolute;
        inset: 0;
        opacity: 0;
        cursor: pointer;
    }

    /* File Queue */
    .file-queue {
        margin-top: var(--space-lg);
        display: flex;
        flex-direction: column;
        gap: var(--space-xs);
    }

    .file-row {
        display: flex;
        align-items: center;
        gap: var(--space-sm);
        padding: var(--space-sm) var(--space-md);
        background: var(--color-surface-2);
        border: 1px solid var(--color-hairline);
        border-radius: var(--radius-md);
        transition: all var(--transition-fast);
    }

    .file-row:hover {
        border-color: var(--color-hairline-strong);
    }

    .file-row.failed {
        border-color: var(--color-error);
        background: var(--color-error-subtle);
    }

    .file-icon-wrap {
        flex-shrink: 0;
        color: var(--color-ink-subtle);
    }

    .file-row:not(.failed) .file-icon-wrap :global(svg) {
        color: var(--color-ink-subtle);
    }

    .file-row.failed .file-icon-wrap :global(svg) {
        color: var(--color-error);
    }

    .file-row .file-icon-wrap :global(svg):first-child {
        color: inherit;
    }

    .file-info {
        flex: 1;
        min-width: 0;
    }

    .file-name-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: var(--space-sm);
    }

    .file-name {
        font-size: 14px;
        font-weight: 500;
        color: var(--color-ink);
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
    }

    .file-size {
        font-size: 12px;
        color: var(--color-ink-tertiary);
        flex-shrink: 0;
    }

    .progress-track {
        width: 100%;
        height: 4px;
        background: var(--color-hairline);
        border-radius: var(--radius-pill);
        overflow: hidden;
        margin-top: var(--space-xs);
    }

    .progress-fill {
        height: 100%;
        background: linear-gradient(90deg, var(--color-primary), var(--color-primary-hover));
        border-radius: var(--radius-pill);
        transition: width var(--transition-base);
    }

    .progress-label {
        font-size: 11px;
        color: var(--color-primary);
        font-weight: 500;
        margin-top: 2px;
        display: block;
    }

    .error-label {
        font-size: 12px;
        color: var(--color-error);
        font-weight: 500;
        margin-top: 2px;
        display: block;
    }

    .file-actions {
        display: flex;
        align-items: center;
        gap: var(--space-xxs);
        flex-shrink: 0;
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
        background: var(--color-surface-3);
        color: var(--color-ink);
        border-color: var(--color-hairline-strong);
    }
</style>
