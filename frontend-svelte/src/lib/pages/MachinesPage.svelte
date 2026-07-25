<script lang="ts">
    import { onMount } from 'svelte';
    import { user } from '../authStore';
    import StatusBadge from '../components/StatusBadge.svelte';
    import Modal from '../components/Modal.svelte';
    import { Plus, Edit, Trash2, Save, Cpu, FileText, Download, Eye, RefreshCw, ChevronRight } from '@lucide/svelte';

    export let showToast: (msg: string, type: 'success' | 'error' | 'warning' | 'info') => void = () => {};
    export let onNavigate: (tab: string) => void = () => {};

    import { apiFetch } from '../api';

    interface MachineFile {
        file_name: string;
        version_no: number;
        uploaded_by: string;
        upload_time?: string;
        created_at?: string;
        file_hash?: string;
    }

    interface Machine {
        id: string;
        name: string;
        type: string;
        manufacturer: string;
        model: string;
        serialNumber: string;
        status: 'Online' | 'Offline' | 'Maintenance' | 'Idle';
        location: string;
        installDate: string;
        lastMaintenance: string;
        files?: MachineFile[];
        loadingFiles?: boolean;
    }

    let machines: Machine[] = [
        { id: '101', name: 'CNC Milling Center', type: '3-Axis CNC Mill', manufacturer: 'Haas', model: 'MillAlpha', serialNumber: 'SN-101-2023', status: 'Online', location: 'Building A - Bay 1', installDate: '2023-01-15', lastMaintenance: '2026-05-15', files: [] },
        { id: '102', name: 'PLC Assembly Line', type: '5-Axis CNC Mill', manufacturer: 'DMG MORI', model: 'LineBeta', serialNumber: 'SN-102-2024', status: 'Idle', location: 'Building A - Bay 2', installDate: '2024-03-20', lastMaintenance: '2026-04-28', files: [] },
        { id: '103', name: 'Precision Lathe', type: 'CNC Lathe', manufacturer: 'Mazak', model: 'LatheGamma', serialNumber: 'SN-103-2022', status: 'Online', location: 'Building B - Bay 1', installDate: '2022-11-10', lastMaintenance: '2026-05-20', files: [] },
    ];

    let showModal = false;
    let editingMachine: Machine | null = null;
    let form: Partial<Machine> = {};

    onMount(() => {
        syncMachinesAndFiles();
    });

    async function syncMachinesAndFiles() {
        try {
            // Fetch live machines if backend is active
            const res = await apiFetch('/machines');
            const data = await res.json();
            if (res.ok && data.machines && data.machines.length > 0) {
                // Merge backend machine IDs
                machines = data.machines.map((m: any) => {
                    const existing = machines.find(x => String(x.id) === String(m.id));
                    return existing || {
                        id: String(m.id),
                        name: m.machine_name,
                        type: 'CNC Processing Machine',
                        manufacturer: 'Haas / Mazak',
                        model: 'V-Series',
                        serialNumber: `SN-${m.id}`,
                        status: 'Online' as const,
                        location: 'Main Factory Floor',
                        installDate: '2023-01-01',
                        lastMaintenance: '2026-05-01',
                        files: [],
                    };
                });
            }
        } catch {
            // Keep default initial machines
        }

        // Fetch uploaded files for each machine
        for (let machine of machines) {
            fetchFilesForMachine(machine.id);
        }
    }

    async function fetchFilesForMachine(machineId: string) {
        machines = machines.map(m => m.id === machineId ? { ...m, loadingFiles: true } : m);
        try {
            const res = await apiFetch(`/files/${machineId}`);
            const data = await res.json();
            if (res.ok && data.files) {
                machines = machines.map(m => m.id === machineId ? { ...m, files: data.files, loadingFiles: false } : m);
            } else {
                machines = machines.map(m => m.id === machineId ? { ...m, files: [], loadingFiles: false } : m);
            }
        } catch {
            // Provide fallback seed files per machine
            let mockFiles: MachineFile[] = [];
            if (machineId === '101') {
                mockFiles = [
                    { file_name: 'pump_housing.nc', version_no: 2, uploaded_by: 'John Doe', upload_time: '2026-07-19T09:42:00' },
                    { file_name: 'bracket_arm.cnc', version_no: 4, uploaded_by: 'Jane Smith', upload_time: '2026-07-17T11:30:00' },
                ];
            } else if (machineId === '102') {
                mockFiles = [
                    { file_name: 'turbine_blade.nc', version_no: 3, uploaded_by: 'Jane Smith', upload_time: '2026-07-19T08:15:00' },
                ];
            } else if (machineId === '103') {
                mockFiles = [
                    { file_name: 'valve_seal.gcode', version_no: 2, uploaded_by: 'Bob Johnson', upload_time: '2026-07-18T16:10:00' },
                ];
            }
            machines = machines.map(m => m.id === machineId ? { ...m, files: mockFiles, loadingFiles: false } : m);
        }
    }

    function statusVariant(status: string): 'success' | 'warning' | 'error' | 'neutral' {
        switch (status) { case 'Online': return 'success'; case 'Maintenance': return 'warning'; case 'Offline': return 'error'; default: return 'neutral'; }
    }

    function openAdd() {
        editingMachine = null;
        form = { name: '', type: '', manufacturer: '', model: '', serialNumber: '', status: 'Online', location: '', installDate: '', lastMaintenance: '' };
        showModal = true;
    }

    function openEdit(machine: Machine) {
        editingMachine = machine;
        form = { ...machine };
        showModal = true;
    }

    function closeModal() { showModal = false; editingMachine = null; }

    function saveMachine() {
        if (!form.name || !form.type) {
            showToast('Please fill required fields', 'error'); return;
        }
        if (editingMachine) {
            machines = machines.map(m => m.id === editingMachine!.id ? { ...m, ...form } as Machine : m);
            showToast(`${form.name} updated`, 'success');
        } else {
            const newId = String(Math.max(...machines.map(m => parseInt(m.id) || 100)) + 1);
            const newM: Machine = { id: newId, files: [], ...form } as Machine;
            machines = [...machines, newM];
            showToast(`${form.name} added`, 'success');
        }
        closeModal();
    }

    function deleteMachine(id: string) {
        const m = machines.find(x => x.id === id);
        machines = machines.filter(x => x.id !== id);
        showToast(`${m?.name} deleted`, 'success');
    }
</script>

<div class="machines-page">
    <div class="card">
        <div class="card-header">
            <div>
                <h3>Machine Fleet & Synchronized Programs</h3>
                <p class="subtitle">Live mapping of machines and uploaded CNC/PLC program files</p>
            </div>
            <div class="header-actions">
                <button class="icon-btn sync-btn" on:click={syncMachinesAndFiles} title="Sync Machines & Files">
                    <RefreshCw size={14} />
                </button>
                {#if $user?.role === 'admin'}
                    <button class="primary-btn" on:click={openAdd}>
                        <Plus size={14} /> Add Machine
                    </button>
                {/if}
            </div>
        </div>

        <div class="machine-list">
            {#each machines as machine}
                <div class="machine-card">
                    <div class="mc-main-info">
                        <div class="mc-header">
                            <div class="mc-id-group">
                                <Cpu size={18} class="mc-icon" />
                                <span class="mc-id">Machine #{machine.id}</span>
                            </div>
                            <StatusBadge variant={statusVariant(machine.status)} dot>{machine.status}</StatusBadge>
                        </div>

                        <h4 class="mc-name">{machine.name}</h4>
                        <p class="mc-type">{machine.type} · {machine.manufacturer} {machine.model}</p>
                        <p class="mc-location">Location: {machine.location}</p>

                        {#if $user?.role === 'admin'}
                            <div class="mc-actions">
                                <button class="icon-btn" on:click={() => openEdit(machine)} title="Edit Machine">
                                    <Edit size={14} />
                                </button>
                                <button class="icon-btn danger" on:click={() => deleteMachine(machine.id)} title="Delete Machine">
                                    <Trash2 size={14} />
                                </button>
                            </div>
                        {/if}
                    </div>

                    <!-- Synchronized Uploaded Files Section -->
                    <div class="mc-files-section">
                        <div class="mc-files-header">
                            <span class="files-title">
                                <FileText size={14} />
                                Synchronized Programs ({machine.files?.length || 0})
                            </span>
                            <button class="link-btn-sm" on:click={() => onNavigate('upload')}>
                                Upload File <ChevronRight size={12} />
                            </button>
                        </div>

                        {#if machine.loadingFiles}
                            <div class="files-loading">Syncing programs...</div>
                        {:else if machine.files && machine.files.length > 0}
                            <div class="files-sublist">
                                {#each machine.files as file}
                                    <div class="file-item-pill">
                                        <div class="f-left">
                                            <FileText size={14} class="f-icon" />
                                            <span class="f-name">{file.file_name}</span>
                                            <StatusBadge variant="brand">v{file.version_no}</StatusBadge>
                                        </div>
                                        <div class="f-right">
                                            <span class="f-meta">By {file.uploaded_by}</span>
                                        </div>
                                    </div>
                                {/each}
                            </div>
                        {:else}
                            <div class="no-files-box">
                                <span>No program files uploaded for Machine #{machine.id} yet.</span>
                            </div>
                        {/if}
                    </div>
                </div>
            {/each}
        </div>
    </div>
</div>

<Modal open={showModal} title={editingMachine ? 'Edit Machine' : 'Add Machine'} size="lg" onClose={closeModal}>
    <form on:submit|preventDefault={saveMachine}>
        <div class="form-grid">
            <div class="form-group">
                <label for="m-name">Name <span class="req">*</span></label>
                <input id="m-name" bind:value={form.name} required placeholder="e.g. CNC Milling Center" />
            </div>
            <div class="form-group">
                <label for="m-type">Type <span class="req">*</span></label>
                <select id="m-type" bind:value={form.type} required>
                    <option value="">Select Type</option>
                    <option>3-Axis CNC Mill</option>
                    <option>5-Axis CNC Mill</option>
                    <option>CNC Lathe</option>
                    <option>CNC Grinder</option>
                    <option>Wire EDM</option>
                    <option>Assembly Line PLC</option>
                </select>
            </div>
            <div class="form-group">
                <label for="m-mfg">Manufacturer</label>
                <input id="m-mfg" bind:value={form.manufacturer} placeholder="e.g. Haas" />
            </div>
            <div class="form-group">
                <label for="m-model">Model</label>
                <input id="m-model" bind:value={form.model} placeholder="e.g. MillAlpha" />
            </div>
            <div class="form-group">
                <label for="m-status">Status</label>
                <select id="m-status" bind:value={form.status}>
                    <option>Online</option>
                    <option>Idle</option>
                    <option>Maintenance</option>
                    <option>Offline</option>
                </select>
            </div>
            <div class="form-group">
                <label for="m-loc">Location</label>
                <input id="m-loc" bind:value={form.location} placeholder="e.g. Building A - Bay 1" />
            </div>
        </div>
    </form>
    <div slot="footer">
        <button class="secondary-btn" on:click={closeModal}>Cancel</button>
        <button class="primary-btn" on:click={saveMachine}>
            <Save size={14} /> {editingMachine ? 'Update' : 'Add Machine'}
        </button>
    </div>
</Modal>

<style>
    .machines-page { max-width: 1080px; }

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

    .card-header h3 { font-size: 18px; font-weight: 600; color: var(--color-ink); margin: 0; }
    .subtitle { font-size: 13px; color: var(--color-ink-subtle); margin: 2px 0 0; }

    .header-actions {
        display: flex;
        align-items: center;
        gap: var(--space-xs);
    }

    .machine-list {
        display: flex;
        flex-direction: column;
        gap: var(--space-lg);
    }

    .machine-card {
        background: var(--color-surface-2);
        border: 1px solid var(--color-hairline);
        border-radius: var(--radius-lg);
        padding: var(--space-md);
        display: grid;
        grid-template-columns: 280px 1fr;
        gap: var(--space-lg);
        transition: border-color var(--transition-fast);
    }

    .machine-card:hover {
        border-color: var(--color-hairline-strong);
    }

    .mc-main-info {
        display: flex;
        flex-direction: column;
        gap: var(--space-xs);
        padding-right: var(--space-md);
        border-right: 1px solid var(--color-hairline);
    }

    .mc-header { display: flex; justify-content: space-between; align-items: center; }
    .mc-id-group { display: flex; align-items: center; gap: 6px; color: var(--color-primary); }
    .mc-id { font-family: var(--font-mono); font-size: 13px; font-weight: 600; color: var(--color-ink); }

    .mc-name { font-size: 16px; font-weight: 600; color: var(--color-ink); margin: 2px 0 0; }
    .mc-type { font-size: 13px; color: var(--color-ink-subtle); margin: 0; }
    .mc-location { font-size: 12px; color: var(--color-ink-tertiary); margin: 0; }

    .mc-actions {
        display: flex;
        gap: var(--space-xs);
        margin-top: auto;
        padding-top: var(--space-xs);
    }

    /* Synchronized Files subpanel */
    .mc-files-section {
        display: flex;
        flex-direction: column;
        gap: var(--space-xs);
    }

    .mc-files-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .files-title {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        font-size: 13px;
        font-weight: 600;
        color: var(--color-ink-muted);
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }

    .link-btn-sm {
        all: unset;
        display: inline-flex;
        align-items: center;
        gap: 2px;
        font-size: 12px;
        font-weight: 500;
        color: var(--color-primary);
        cursor: pointer;
    }

    .link-btn-sm:hover {
        color: var(--color-primary-hover);
    }

    .files-sublist {
        display: flex;
        flex-direction: column;
        gap: 6px;
    }

    .file-item-pill {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 8px 12px;
        background: var(--color-surface-1);
        border: 1px solid var(--color-hairline);
        border-radius: var(--radius-md);
        font-size: 13px;
    }

    .f-left {
        display: flex;
        align-items: center;
        gap: var(--space-xs);
    }

    .f-icon {
        color: var(--color-primary);
        flex-shrink: 0;
    }

    .f-name {
        font-family: var(--font-mono);
        font-weight: 500;
        color: var(--color-ink);
    }

    .f-right {
        display: flex;
        align-items: center;
        gap: var(--space-sm);
    }

    .f-meta {
        font-size: 12px;
        color: var(--color-ink-tertiary);
    }

    .no-files-box, .files-loading {
        padding: var(--space-md);
        background: var(--color-surface-1);
        border: 1px dashed var(--color-hairline);
        border-radius: var(--radius-md);
        font-size: 13px;
        color: var(--color-ink-tertiary);
        text-align: center;
    }

    .icon-btn {
        display: flex; align-items: center; justify-content: center;
        width: 30px; height: 30px;
        border: 1px solid var(--color-hairline); background: var(--color-surface-1);
        color: var(--color-ink-subtle); border-radius: var(--radius-sm);
        cursor: pointer; transition: all var(--transition-fast);
    }
    .icon-btn:hover { background: var(--color-surface-3); color: var(--color-ink); border-color: var(--color-hairline-strong); }
    .icon-btn.danger:hover { background: var(--color-error-subtle); color: var(--color-error); }

    .primary-btn {
        padding: 8px 16px; background: var(--color-primary); color: var(--color-on-primary);
        border: none; border-radius: var(--radius-md); font-size: 14px; font-weight: 500;
        cursor: pointer; display: inline-flex; align-items: center; gap: var(--space-xs);
        transition: background var(--transition-fast);
    }
    .primary-btn:hover { background: var(--color-primary-hover); }

    .secondary-btn {
        padding: 8px 16px; border: 1px solid var(--color-hairline); background: transparent;
        color: var(--color-ink-subtle); font-size: 14px; font-weight: 500;
        border-radius: var(--radius-md); cursor: pointer; transition: all var(--transition-fast);
    }
    .secondary-btn:hover { background: var(--color-surface-2); color: var(--color-ink); }

    .form-grid { display: grid; grid-template-columns: 1fr 1fr; gap: var(--space-md); }
    .form-group label { display: block; font-size: 13px; font-weight: 500; color: var(--color-ink-subtle); margin-bottom: var(--space-xs); }
    .req { color: var(--color-error); }

    @media (max-width: 860px) {
        .machine-card { grid-template-columns: 1fr; }
        .mc-main-info { border-right: none; border-bottom: 1px solid var(--color-hairline); padding-right: 0; padding-bottom: var(--space-md); }
    }
</style>
