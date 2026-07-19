<script lang="ts">
    export let variant: 'success' | 'warning' | 'error' | 'neutral' | 'info' | 'brand' = 'neutral';
    export let size: 'sm' | 'md' = 'sm';
    export let dot: boolean = false;
</script>

<span class="badge {variant} {size}" class:has-dot={dot}>
    {#if dot}
        <span class="dot"></span>
    {/if}
    <slot />
</span>

<style>
    .badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 2px 8px;
        border-radius: var(--radius-pill);
        font-size: 11px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.04em;
        line-height: 1.4;
        white-space: nowrap;
    }

    .badge.md {
        padding: 4px 12px;
        font-size: 12px;
    }

    .dot {
        width: 6px;
        height: 6px;
        border-radius: var(--radius-full);
        flex-shrink: 0;
    }

    /* Variants */
    .neutral {
        background: var(--color-surface-2);
        color: var(--color-ink-muted);
    }
    .neutral .dot { background: var(--color-ink-subtle); }

    .success {
        background: var(--color-success-subtle);
        color: var(--color-success);
    }
    .success .dot { background: var(--color-success); }

    .warning {
        background: var(--color-warning-subtle);
        color: var(--color-warning);
    }
    .warning .dot { background: var(--color-warning); }

    .error {
        background: var(--color-error-subtle);
        color: var(--color-error);
    }
    .error .dot { background: var(--color-error); }

    .info {
        background: var(--color-info-subtle);
        color: var(--color-info);
    }
    .info .dot { background: var(--color-info); }

    .brand {
        background: rgba(94, 106, 210, 0.12);
        color: var(--color-primary);
    }
    .brand .dot { background: var(--color-primary); }
</style>
