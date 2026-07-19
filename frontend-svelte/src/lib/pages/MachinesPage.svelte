<script lang="ts">
    import { user } from '../authStore';
    import StatusBadge from '../components/StatusBadge.svelte';
    import Modal from '../components/Modal.svelte';
    import { Plus, Edit, Trash2, Save, Cpu } from '@lucide/svelte';

    export let showToast: (msg: string, type: 'success' | 'error' | 'warning' | 'info') => void = () => {};

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
        programCount: number;
        lastUpload: string;
    }

    let machines: Machine[] = [
        { id: '101', name: 'Pump Housing Cell', type: '3-Axis CNC Mill', manufacturer: 'Haas', model: 'VF-2SS', serialNumber: 'SN-101-2023', status: 'Online', location: 'Building A - Bay 1', installDate: '2023-01-15', lastMaintenance: '2026-05-15', programCount: 18, lastUpload: '2 hours ago' },
        { id: '102', name: 'Turbine Blade Cell', type: '5-Axis CNC Mill', manufacturer: 'DMG MORI', model: 'NHX 5000', serialNumber: 'SN-102-2024', status: 'Idle', location: 'Building A - Bay 2', installDate: '2024-03-20', lastMaintenance: '2026-04-28', programCount: 22, lastUpload: 'Yesterday' },
        { id: '103', name: 'Valve Seal Cell', type: 'CNC Lathe', manufacturer: 'Mazak', model: 'Quick Turn 250M', serialNumber: 'SN-103-2022', status: 'Online', location: 'Building B - Bay 1', installDate: '2022-11-10', lastMaintenance: '2026-05-20', programCount: 11, lastUpload: '3 hours ago' },
        { id: '104', name: 'Seal Calibration Cell', type: 'CNC Grinder', manufacturer: 'Studer', model: 'S33', serialNumber: 'SN-104-2021', status: 'Maintenance', location: 'Building B - Bay 3', installDate: '2021-08-05', lastMaintenance: '2026-03-10', programCount: 9, lastUpload: '4 days ago' },
    ];

    let showModal = false;
    let editingMachine: Machine | null = null;
    let form: Partial<Machine> = {};

    function statusVariant(status: string): 'success' | 'warning' | 'error' | 'neutral' {
        switch (status) { case 'Online': return 'success'; case 'Maintenance': return 'warning'; case 'Offline': return 'error'; default: return 'neutral'; }
    }

    function openAdd() {
        editingMachine = null;
        form = { name: '', type: '', manufacturer: '', model: '', serialNumber: '', status: 'Offline', location: '', installDate: '', lastMaintenance: '' };
        showModal = true;
    }

    function openEdit(machine: Machine) {
        editingMachine = machine;
        form = { ...machine };
        showModal = true;
    }

    function closeModal() { showModal = false; editingMachine = null; }

    function saveMachine() {
        if (!form.name || !form.type || !form.manufacturer) {
            showToast('Please fill required fields', 'error'); return;
        }
        if (editingMachine) {
            machines = machines.map(m => m.id === editingMachine!.id ? { ...m, ...form } as Machine : m);
            showToast(`${form.name} updated`, 'success');
        } else {
            const newM: Machine = { id: String(Math.max(...machines.map(m => parseInt(m.id))) + 1), programCount: 0, lastUpload: 'Never', ...form } as Machine;
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
            <h3>Machine Fleet</h3>
            {#if $user?.role === 'admin'}
                <button class="primary-btn" on:click={openAdd}>
                    <Plus size={14} /> Add Machine
                </button>
            {/if}
        </div>

        <div class="machine-grid">
            {#each machines as machine}
                <div class="machine-card">
                    <div class="mc-header">
                        <div class="mc-id">#{machine.id}</div>
                        <StatusBadge variant={statusVariant(machine.status)} dot>{machine.status}</StatusBadge>
                    </div>
                    <h4 class="mc-name">{machine.name}</h4>
                    <p class="mc-type">{machine.type} · {machine.manufacturer} {machine.model}</p>
                    <div class="mc-meta">
                        <span>{machine.location}</span>
                        <span>{machine.programCount} programs</span>
                        <span>Last upload: {machine.lastUpload}</span>
                    </div>
                    {#if $user?.role === 'admin'}
                        <div class="mc-actions">
                            <button class="icon-btn" on:click={() => openEdit(machine)} title="Edit">
                                <Edit size={14} />
                            </button>
                            <button class="icon-btn danger" on:click={() => deleteMachine(machine.id)} title="Delete">
                                <Trash2 size={14} />
                            </button>
                        </div>
                    {/if}
                </div>
            {/each}
        </div>
    </div>
</div>

<Modal open={showModal} title={editingMachine ? 'Edit Machine' : 'Add Machine'} size="lg" onClose={closeModal}>
    <form on:submit|preventDefault={saveMachine}>
        <div class="form-grid">
            <div class="form-group">
                <label>Name <span class="req">*</span></label>
                <input bind:value={form.name} required placeholder="e.g. Pump Housing Cell" />
            </div>
            <div class="form-group">
                <label>Type <span class="req">*</span></label>
                <select bind:value={form.type} required>
                    <option value="">Select</option>
                    <option>3-Axis CNC Mill</option><option>5-Axis CNC Mill</option>
                    <option>CNC Lathe</option><option>CNC Grinder</option>
                    <option>CNC Router</option><option>Wire EDM</option><option>Other</option>
                </select>
            </div>
            <div class="form-group">
                <label>Manufacturer <span class="req">*</span></label>
                <input bind:value={form.manufacturer} required placeholder="e.g. Haas" />
            </div>
            <div class="form-group">
                <label>Model</label>
                <input bind:value={form.model} placeholder="e.g. VF-2SS" />
            </div>
            <div class="form-group">
                <label>Serial Number</label>
                <input bind:value={form.serialNumber} placeholder="e.g. SN-101-2023" />
            </div>
            <div class="form-group">
                <label>Status</label>
                <select bind:value={form.status}>
                    <option>Online</option><option>Offline</option><option>Idle</option><option>Maintenance</option>
                </select>
            </div>
            <div class="form-group full">
                <label>Location</label>
                <input bind:value={form.location} placeholder="e.g. Building A - Bay 1" />
            </div>
            <div class="form-group">
                <label>Install Date</label>
                <input type="date" bind:value={form.installDate} />
            </div>
            <div class="form-group">
                <label>Last Maintenance</label>
                <input type="date" bind:value={form.lastMaintenance} />
            </div>
        </div>
    </form>
    <div slot="footer">
        <button class="secondary-btn" on:click={closeModal}>Cancel</button>
        <button class="primary-btn" on:click={saveMachine}>
            <Save size={14} /> {editingMachine ? 'Update' : 'Add'}
        </button>
    </div>
</Modal>

<style>
    .machines-page { max-width: 1100px; }

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
    .card-header h3 { font-size: 18px; font-weight: 600; color: var(--color-ink); margin: 0; }

    .machine-grid {
        display: grid;
        gap: var(--space-md);
        grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    }

    .machine-card {
        background: var(--color-surface-2);
        border: 1px solid var(--color-hairline);
        border-radius: var(--radius-lg);
        padding: var(--space-md);
        display: flex;
        flex-direction: column;
        gap: var(--space-xs);
        transition: border-color var(--transition-fast);
    }

    .machine-card:hover { border-color: var(--color-hairline-strong); }

    .mc-header { display: flex; justify-content: space-between; align-items: center; }
    .mc-id { font-family: var(--font-mono); font-size: 12px; color: var(--color-ink-tertiary); }
    .mc-name { font-size: 15px; font-weight: 600; color: var(--color-ink); margin: 0; }
    .mc-type { font-size: 13px; color: var(--color-ink-subtle); margin: 0; }
    .mc-meta { display: flex; flex-direction: column; gap: 2px; font-size: 12px; color: var(--color-ink-tertiary); margin-top: var(--space-xxs); }

    .mc-actions {
        display: flex;
        gap: var(--space-xs);
        margin-top: var(--space-xs);
        padding-top: var(--space-xs);
        border-top: 1px solid var(--color-hairline);
    }

    .icon-btn {
        display: flex; align-items: center; justify-content: center;
        width: 28px; height: 28px;
        border: 1px solid var(--color-hairline); background: transparent;
        color: var(--color-ink-subtle); border-radius: var(--radius-sm);
        cursor: pointer; transition: all var(--transition-fast);
    }
    .icon-btn:hover { background: var(--color-surface-3); color: var(--color-ink); }
    .icon-btn.danger { color: var(--color-error); }
    .icon-btn.danger:hover { background: var(--color-error-subtle); }

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
    .form-group.full { grid-column: 1 / -1; }
    .req { color: var(--color-error); }

    @media (max-width: 768px) { .form-grid { grid-template-columns: 1fr; } }
</style>
