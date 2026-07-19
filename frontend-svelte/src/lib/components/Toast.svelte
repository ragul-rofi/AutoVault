<script lang="ts">
    import { toasts, removeToast, type ToastItem } from '../stores/toastStore';
    import { CheckCircle, AlertTriangle, XCircle, Info, X } from '@lucide/svelte';

    const iconMap = {
        success: CheckCircle,
        error: XCircle,
        warning: AlertTriangle,
        info: Info,
    };
</script>

<div class="toast-container" aria-live="polite">
    {#each $toasts as toast (toast.id)}
        <div class="toast {toast.type}" role="alert">
            <svelte:component this={iconMap[toast.type]} size={18} class="toast-icon" />
            <span class="toast-message">{toast.message}</span>
            <button class="toast-close" on:click={() => removeToast(toast.id)} aria-label="Dismiss">
                <X size={14} />
            </button>
        </div>
    {/each}
</div>

<style>
    .toast-container {
        position: fixed;
        top: var(--space-lg);
        right: var(--space-lg);
        z-index: 9999;
        display: flex;
        flex-direction: column;
        gap: var(--space-xs);
        pointer-events: none;
        max-width: 420px;
        width: 100%;
    }

    .toast {
        display: flex;
        align-items: center;
        gap: var(--space-sm);
        padding: var(--space-sm) var(--space-md);
        background: var(--color-surface-1);
        border: 1px solid var(--color-hairline);
        border-radius: var(--radius-lg);
        color: var(--color-ink);
        font-size: 14px;
        font-weight: 500;
        pointer-events: all;
        animation: slideDown 300ms cubic-bezier(0.34, 1.56, 0.64, 1);
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.3);
    }

    .toast.success { border-left: 3px solid var(--color-success); }
    .toast.success :global(.toast-icon) { color: var(--color-success); }
    .toast.error { border-left: 3px solid var(--color-error); }
    .toast.error :global(.toast-icon) { color: var(--color-error); }
    .toast.warning { border-left: 3px solid var(--color-warning); }
    .toast.warning :global(.toast-icon) { color: var(--color-warning); }
    .toast.info { border-left: 3px solid var(--color-primary); }
    .toast.info :global(.toast-icon) { color: var(--color-primary); }

    .toast-message { flex: 1; line-height: 1.4; }

    .toast-close {
        display: flex; align-items: center; justify-content: center;
        width: 24px; height: 24px; border: none; background: transparent;
        color: var(--color-ink-subtle); border-radius: var(--radius-sm);
        cursor: pointer; flex-shrink: 0; transition: all var(--transition-fast);
    }
    .toast-close:hover { background: var(--color-surface-2); color: var(--color-ink); }

    @keyframes slideDown {
        from { opacity: 0; transform: translateY(-12px) scale(0.95); }
        to { opacity: 1; transform: translateY(0) scale(1); }
    }

    @media (max-width: 480px) {
        .toast-container { left: var(--space-md); right: var(--space-md); max-width: none; }
    }
</style>
