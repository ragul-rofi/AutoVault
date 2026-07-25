<script lang="ts">
    import { createEventDispatcher } from 'svelte';
    import { X } from '@lucide/svelte';

    export let open: boolean = false;
    export let size: 'sm' | 'md' | 'lg' = 'md';
    export let title: string = '';
    export let onClose: () => void = () => {};

    const dispatch = createEventDispatcher();
    const sizeMap = { sm: '480px', md: '640px', lg: '800px' };

    function handleClose() {
        if (onClose) onClose();
        dispatch('close');
    }

    function handleOverlayClick() {
        handleClose();
    }

    function handleKeydown(e: KeyboardEvent) {
        if (e.key === 'Escape') handleClose();
    }
</script>

<svelte:window on:keydown={handleKeydown} />

{#if open}
    <div class="modal-overlay" on:click={handleOverlayClick} role="dialog" aria-modal="true">
        <div
            class="modal-panel"
            style="max-width: {sizeMap[size]}"
            on:click|stopPropagation
        >
            {#if title || $$slots.header}
                <div class="modal-header">
                    {#if $$slots.header}
                        <slot name="header" />
                    {:else}
                        <h3>{title}</h3>
                    {/if}
                    <button class="close-btn" on:click={handleClose} type="button" aria-label="Close">
                        <X size={18} />
                    </button>
                </div>
            {/if}

            <div class="modal-body">
                <slot />
            </div>

            {#if $$slots.footer}
                <div class="modal-footer">
                    <slot name="footer" />
                </div>
            {/if}
        </div>
    </div>
{/if}

<style>
    .modal-overlay {
        position: fixed;
        inset: 0;
        background: var(--color-overlay);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 1000;
        padding: 20px;
        animation: fadeIn 150ms ease;
    }

    .modal-panel {
        background: var(--color-surface-1);
        border: 1px solid var(--color-hairline);
        border-radius: var(--radius-xl);
        width: 100%;
        max-height: 90vh;
        overflow-y: auto;
        animation: slideUp 200ms cubic-bezier(0.34, 1.56, 0.64, 1);
    }

    .modal-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: var(--space-lg);
        border-bottom: 1px solid var(--color-hairline);
    }

    .modal-header h3 {
        font-size: 18px;
        font-weight: 600;
        color: var(--color-ink);
        margin: 0;
    }

    .close-btn {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 32px;
        height: 32px;
        border: none;
        background: transparent;
        color: var(--color-ink-subtle);
        border-radius: var(--radius-md);
        cursor: pointer;
        transition: all var(--transition-fast);
    }

    .close-btn:hover {
        background: var(--color-surface-2);
        color: var(--color-ink);
    }

    .modal-body {
        padding: var(--space-lg);
    }

    .modal-footer {
        display: flex;
        align-items: center;
        justify-content: flex-end;
        gap: var(--space-sm);
        padding: var(--space-lg);
        border-top: 1px solid var(--color-hairline);
    }

    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }

    @keyframes slideUp {
        from { opacity: 0; transform: translateY(16px) scale(0.97); }
        to { opacity: 1; transform: translateY(0) scale(1); }
    }
</style>
