<script lang="ts">
    import { createEventDispatcher } from 'svelte';

    export let icon: any = null;
    export let title: string = 'No data yet';
    export let description: string = '';
    export let actionLabel: string = '';

    const dispatch = createEventDispatcher();
</script>

<div class="empty-state">
    {#if icon}
        <div class="empty-icon">
            <svelte:component this={icon} size={48} strokeWidth={1.25} />
        </div>
    {/if}
    <p class="empty-title">{title}</p>
    {#if description}
        <p class="empty-description">{description}</p>
    {/if}
    {#if actionLabel}
        <button class="empty-action" on:click={() => dispatch('action')}>
            {actionLabel}
        </button>
    {/if}
</div>

<style>
    .empty-state {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: var(--space-xxl) var(--space-lg);
        text-align: center;
        min-height: 200px;
    }

    .empty-icon {
        color: var(--color-ink-tertiary);
        margin-bottom: var(--space-md);
        opacity: 0.5;
    }

    .empty-title {
        font-size: 16px;
        font-weight: 500;
        color: var(--color-ink-subtle);
        margin: 0 0 var(--space-xs);
    }

    .empty-description {
        font-size: 14px;
        color: var(--color-ink-tertiary);
        max-width: 360px;
        margin: 0;
    }

    .empty-action {
        margin-top: var(--space-md);
        padding: 8px 16px;
        background: var(--color-primary);
        color: var(--color-on-primary);
        border: none;
        border-radius: var(--radius-md);
        font-size: 14px;
        font-weight: 500;
        cursor: pointer;
        transition: background var(--transition-fast);
    }

    .empty-action:hover {
        background: var(--color-primary-hover);
    }
</style>
