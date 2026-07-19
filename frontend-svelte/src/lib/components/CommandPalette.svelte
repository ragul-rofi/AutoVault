<script lang="ts">
    import { onMount } from 'svelte';
    import {
        Search, LayoutDashboard, Upload, List, RotateCcw, ArrowLeftRight,
        Settings, BarChart3, Users, Activity, Shield, FileText, Cpu, ArrowRight
    } from '@lucide/svelte';

    export let open: boolean = false;
    export let onClose: () => void = () => {};
    export let onAction: (action: CommandOrFileAction) => void = () => {};

    let query = '';
    let selectedIndex = 0;
    let inputEl: HTMLInputElement;

    export interface CommandOrFileAction {
        id: string;
        type: 'navigation' | 'file';
        label: string;
        description?: string;
        icon: any;
        category: string;
        shortcut?: string;
        fileData?: any;
    }

    const navigationCommands: CommandOrFileAction[] = [
        { id: 'overview', type: 'navigation', label: 'Go to Overview', icon: LayoutDashboard, category: 'Pages', shortcut: 'G O' },
        { id: 'view', type: 'navigation', label: 'File Browser & Programs', icon: List, category: 'Pages', shortcut: 'G F' },
        { id: 'upload', type: 'navigation', label: 'Upload Program File', icon: Upload, category: 'Pages', shortcut: 'G U' },
        { id: 'machines', type: 'navigation', label: 'Machine Fleet', icon: Settings, category: 'Pages', shortcut: 'G M' },
        { id: 'analytics', type: 'navigation', label: 'Analytics & Intelligence', icon: BarChart3, category: 'Pages' },
        { id: 'audit', type: 'navigation', label: 'Audit Trail & Logs', icon: Activity, category: 'Pages' },
        { id: 'rollback', type: 'navigation', label: 'Rollback Version', icon: RotateCcw, category: 'Pages' },
        { id: 'compare', type: 'navigation', label: 'Compare Versions', icon: ArrowLeftRight, category: 'Pages' },
        { id: 'access', type: 'navigation', label: 'Access Control', icon: Users, category: 'Pages' },
        { id: 'settings', type: 'navigation', label: 'Settings', icon: Shield, category: 'Pages' },
    ];

    // Default program files list for direct search & preview
    const knownFiles: CommandOrFileAction[] = [
        { id: 'file-pump-housing', type: 'file', label: 'pump_housing.nc', description: 'Machine 101 · v2 · Haas VF-2SS', icon: FileText, category: 'Files & Programs', fileData: { file_name: 'pump_housing.nc', machine_id: 101, version_no: 2, uploaded_by: 'John Doe', upload_time: '2026-07-19T09:42:00', file_hash: 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855' } },
        { id: 'file-turbine-blade', type: 'file', label: 'turbine_blade.nc', description: 'Machine 102 · v3 · DMG MORI', icon: FileText, category: 'Files & Programs', fileData: { file_name: 'turbine_blade.nc', machine_id: 102, version_no: 3, uploaded_by: 'Jane Smith', upload_time: '2026-07-19T08:15:00', file_hash: '8f434346648f6b96df89dda901c5176b10a6d83961dd3c1ac88b59b2dc327aa4' } },
        { id: 'file-valve-seal', type: 'file', label: 'valve_seal.gcode', description: 'Machine 103 · v2 · Mazak Quick Turn', icon: FileText, category: 'Files & Programs', fileData: { file_name: 'valve_seal.gcode', machine_id: 103, version_no: 2, uploaded_by: 'Bob Johnson', upload_time: '2026-07-18T16:10:00', file_hash: 'dca7be1180a6f4b1bf123782d5716d89916d924f2ee38510a526ab433500f756' } },
        { id: 'file-bracket-arm', type: 'file', label: 'bracket_arm.cnc', description: 'Machine 101 · v4 · Haas VF-2SS', icon: FileText, category: 'Files & Programs', fileData: { file_name: 'bracket_arm.cnc', machine_id: 101, version_no: 4, uploaded_by: 'Jane Smith', upload_time: '2026-07-17T11:30:00', file_hash: '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8' } },
    ];

    $: allItems = [...knownFiles, ...navigationCommands];

    $: filteredCommands = query.trim()
        ? allItems.filter(item =>
            `${item.label} ${item.description || ''} ${item.category}`
                .toLowerCase()
                .includes(query.trim().toLowerCase())
        )
        : allItems;

    $: selectedIndex = Math.min(selectedIndex, Math.max(filteredCommands.length - 1, 0));

    $: groupedCommands = filteredCommands.reduce((groups, cmd) => {
        if (!groups[cmd.category]) groups[cmd.category] = [];
        groups[cmd.category].push(cmd);
        return groups;
    }, {} as Record<string, CommandOrFileAction[]>);

    function handleKeydown(e: KeyboardEvent) {
        if (e.key === 'Escape') {
            onClose();
            return;
        }
        if (e.key === 'ArrowDown') {
            e.preventDefault();
            selectedIndex = Math.min(selectedIndex + 1, filteredCommands.length - 1);
        }
        if (e.key === 'ArrowUp') {
            e.preventDefault();
            selectedIndex = Math.max(selectedIndex - 1, 0);
        }
        if (e.key === 'Enter' && filteredCommands[selectedIndex]) {
            e.preventDefault();
            onAction(filteredCommands[selectedIndex]);
            onClose();
        }
    }

    function selectCommand(cmd: CommandOrFileAction) {
        onAction(cmd);
        onClose();
    }

    $: if (open && inputEl) {
        query = '';
        selectedIndex = 0;
        setTimeout(() => inputEl?.focus(), 50);
    }
</script>

{#if open}
    <div class="palette-overlay" on:click={onClose} on:keydown={handleKeydown} role="dialog" aria-modal="true">
        <div class="palette-panel" on:click|stopPropagation>
            <div class="palette-input-wrapper">
                <Search size={18} />
                <input
                    bind:this={inputEl}
                    bind:value={query}
                    on:keydown={handleKeydown}
                    type="text"
                    placeholder="Search program files (e.g. pump_housing.nc) or pages..."
                    spellcheck="false"
                    autocomplete="off"
                />
            </div>

            <div class="palette-results">
                {#if filteredCommands.length > 0}
                    {#each Object.entries(groupedCommands) as [category, cmds]}
                        <div class="palette-group">
                            <span class="palette-group-label">{category}</span>
                            {#each cmds as cmd}
                                {@const flatIndex = filteredCommands.indexOf(cmd)}
                                <button
                                    class="palette-item"
                                    class:selected={flatIndex === selectedIndex}
                                    on:click={() => selectCommand(cmd)}
                                    on:mouseenter={() => selectedIndex = flatIndex}
                                >
                                    <svelte:component this={cmd.icon} size={16} />
                                    <div class="palette-item-text">
                                        <span class="palette-item-label">{cmd.label}</span>
                                        {#if cmd.description}
                                            <span class="palette-item-desc">{cmd.description}</span>
                                        {/if}
                                    </div>
                                    {#if cmd.type === 'file'}
                                        <span class="badge-preview">Preview File</span>
                                    {:else if cmd.shortcut}
                                        <span class="palette-shortcut">{cmd.shortcut}</span>
                                    {/if}
                                </button>
                            {/each}
                        </div>
                    {/each}
                {:else}
                    <div class="palette-empty">No matching files or commands found</div>
                {/if}
            </div>
        </div>
    </div>
{/if}

<style>
    .palette-overlay {
        position: fixed;
        inset: 0;
        background: var(--color-overlay);
        display: flex;
        align-items: flex-start;
        justify-content: center;
        padding-top: 12vh;
        z-index: 2000;
        animation: fadeIn 100ms ease;
    }

    .palette-panel {
        width: 100%;
        max-width: 580px;
        background: var(--color-surface-1);
        border: 1px solid var(--color-hairline);
        border-radius: var(--radius-xl);
        overflow: hidden;
        animation: paletteIn 200ms cubic-bezier(0.34, 1.56, 0.64, 1);
        box-shadow: 0 16px 70px rgba(0, 0, 0, 0.5);
    }

    .palette-input-wrapper {
        display: flex;
        align-items: center;
        gap: var(--space-sm);
        padding: var(--space-md) var(--space-lg);
        border-bottom: 1px solid var(--color-hairline);
        color: var(--color-ink-subtle);
    }

    .palette-input-wrapper input {
        flex: 1;
        border: none;
        background: transparent;
        font-size: 15px;
        color: var(--color-ink);
        outline: none;
        padding: 0;
    }

    .palette-input-wrapper input::placeholder {
        color: var(--color-ink-tertiary);
    }

    .palette-results {
        max-height: 420px;
        overflow-y: auto;
        padding: var(--space-xs);
    }

    .palette-group {
        padding: var(--space-xxs) 0;
    }

    .palette-group-label {
        display: block;
        padding: var(--space-xs) var(--space-sm);
        font-size: 11px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: var(--color-ink-tertiary);
    }

    .palette-item {
        display: flex;
        align-items: center;
        gap: var(--space-sm);
        width: 100%;
        padding: 10px var(--space-sm);
        border: none;
        background: transparent;
        color: var(--color-ink-muted);
        font-size: 14px;
        font-weight: 400;
        border-radius: var(--radius-md);
        cursor: pointer;
        transition: background var(--transition-fast);
        text-align: left;
    }

    .palette-item:hover,
    .palette-item.selected {
        background: var(--color-surface-2);
        color: var(--color-ink);
    }

    .palette-item :global(svg) {
        flex-shrink: 0;
        opacity: 0.7;
    }

    .palette-item.selected :global(svg) {
        opacity: 1;
        color: var(--color-primary);
    }

    .palette-item-text {
        flex: 1;
        display: flex;
        flex-direction: column;
        min-width: 0;
    }

    .palette-item-label {
        font-weight: 500;
    }

    .palette-item-desc {
        font-size: 12px;
        color: var(--color-ink-tertiary);
    }

    .badge-preview {
        font-size: 11px;
        font-weight: 600;
        background: rgba(94, 106, 210, 0.15);
        color: var(--color-primary);
        padding: 2px 8px;
        border-radius: var(--radius-pill);
    }

    .palette-shortcut {
        font-size: 12px;
        color: var(--color-ink-tertiary);
        font-family: var(--font-mono);
    }

    .palette-empty {
        padding: var(--space-xl);
        text-align: center;
        color: var(--color-ink-tertiary);
        font-size: 14px;
    }

    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }

    @keyframes paletteIn {
        from { opacity: 0; transform: translateY(-8px) scale(0.97); }
        to { opacity: 1; transform: translateY(0) scale(1); }
    }
</style>
