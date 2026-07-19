<script lang="ts">
    import { Search, LayoutDashboard, Upload, List, RotateCcw, ArrowLeftRight, Settings, BarChart3, Users, Activity, Shield, FileText, Cpu } from '@lucide/svelte';

    export let open: boolean = false;
    export let onClose: () => void = () => {};
    export let onAction: (action: CommandAction) => void = () => {};

    let query = '';
    let selectedIndex = 0;
    let inputEl: HTMLInputElement;

    interface CommandAction {
        id: string;
        label: string;
        description?: string;
        icon: any;
        category: string;
        shortcut?: string;
    }

    const commands: CommandAction[] = [
        { id: 'overview', label: 'Go to Overview', icon: LayoutDashboard, category: 'Navigation', shortcut: 'G O' },
        { id: 'upload', label: 'Upload File', icon: Upload, category: 'Navigation', shortcut: 'G U' },
        { id: 'view', label: 'View Files', icon: List, category: 'Navigation', shortcut: 'G F' },
        { id: 'rollback', label: 'Rollback Version', icon: RotateCcw, category: 'Navigation' },
        { id: 'compare', label: 'Compare Versions', icon: ArrowLeftRight, category: 'Navigation' },
        { id: 'machines', label: 'Machine Management', icon: Settings, category: 'Navigation', shortcut: 'G M' },
        { id: 'analytics', label: 'Analytics & Reports', icon: BarChart3, category: 'Navigation' },
        { id: 'audit', label: 'Audit Trail', icon: Activity, category: 'Navigation' },
        { id: 'access', label: 'Access Control', icon: Users, category: 'Navigation' },
        { id: 'settings', label: 'Settings', icon: Shield, category: 'Navigation' },
    ];

    $: filteredCommands = query.trim()
        ? commands.filter(cmd =>
            `${cmd.label} ${cmd.description || ''} ${cmd.category}`
                .toLowerCase()
                .includes(query.trim().toLowerCase())
        )
        : commands;

    $: selectedIndex = Math.min(selectedIndex, Math.max(filteredCommands.length - 1, 0));

    $: groupedCommands = filteredCommands.reduce((groups, cmd) => {
        if (!groups[cmd.category]) groups[cmd.category] = [];
        groups[cmd.category].push(cmd);
        return groups;
    }, {} as Record<string, CommandAction[]>);

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

    function selectCommand(cmd: CommandAction) {
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
                    placeholder="Type a command or search..."
                    spellcheck="false"
                    autocomplete="off"
                />
            </div>

            <div class="palette-results">
                {#if filteredCommands.length > 0}
                    {#each Object.entries(groupedCommands) as [category, cmds]}
                        <div class="palette-group">
                            <span class="palette-group-label">{category}</span>
                            {#each cmds as cmd, i}
                                {@const flatIndex = filteredCommands.indexOf(cmd)}
                                <button
                                    class="palette-item"
                                    class:selected={flatIndex === selectedIndex}
                                    on:click={() => selectCommand(cmd)}
                                    on:mouseenter={() => selectedIndex = flatIndex}
                                >
                                    <svelte:component this={cmd.icon} size={16} />
                                    <span class="palette-item-label">{cmd.label}</span>
                                    {#if cmd.shortcut}
                                        <span class="palette-shortcut">{cmd.shortcut}</span>
                                    {/if}
                                </button>
                            {/each}
                        </div>
                    {/each}
                {:else}
                    <div class="palette-empty">No results found</div>
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
        padding-top: 15vh;
        z-index: 2000;
        animation: fadeIn 100ms ease;
    }

    .palette-panel {
        width: 100%;
        max-width: 560px;
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
        font-size: 16px;
        color: var(--color-ink);
        outline: none;
        padding: 0;
    }

    .palette-input-wrapper input::placeholder {
        color: var(--color-ink-tertiary);
    }

    .palette-results {
        max-height: 400px;
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
        opacity: 0.6;
    }

    .palette-item.selected :global(svg) {
        opacity: 1;
        color: var(--color-primary);
    }

    .palette-item-label {
        flex: 1;
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
