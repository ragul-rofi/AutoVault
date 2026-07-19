<script lang="ts">
    import { Search, X, Command } from '@lucide/svelte';

    export let pageTitle: string = '';
    export let searchQuery: string = '';
    export let onSearchChange: (query: string) => void = () => {};
    export let onCommandPalette: () => void = () => {};

    let searchWrapperElement: HTMLElement;
    let showSearchResults = false;

    function clearSearch() {
        searchQuery = '';
        onSearchChange('');
        showSearchResults = false;
    }

    function handleClickOutside(event: MouseEvent) {
        if (searchWrapperElement && !searchWrapperElement.contains(event.target as Node)) {
            showSearchResults = false;
        }
    }
</script>

<svelte:window on:click={handleClickOutside} />

<header class="topbar">
    <h2 class="page-title">{pageTitle}</h2>

    <div class="search-wrapper" bind:this={searchWrapperElement}>
        <div class="search-box" on:click={onCommandPalette} role="button" tabindex="0" on:keydown={(e) => e.key === 'Enter' && onCommandPalette()}>
            <Search size={16} />
            <span class="search-placeholder">Search or jump to...</span>
            <div class="search-shortcut">
                <kbd>⌘</kbd><kbd>K</kbd>
            </div>
        </div>
    </div>

    <div class="topbar-actions">
        <slot name="actions" />
    </div>
</header>

<style>
    .topbar {
        position: sticky;
        top: 0;
        z-index: 40;
        display: flex;
        align-items: center;
        gap: var(--space-md);
        min-height: var(--topbar-height);
        padding: 0 var(--space-xl);
        background: var(--color-surface-1);
        border-bottom: 1px solid var(--color-hairline);
    }

    .page-title {
        font-size: 16px;
        font-weight: 600;
        color: var(--color-ink);
        white-space: nowrap;
        letter-spacing: -0.3px;
        margin: 0;
    }

    .search-wrapper {
        flex: 1;
        max-width: 480px;
        margin: 0 auto;
    }

    .search-box {
        display: flex;
        align-items: center;
        gap: var(--space-sm);
        padding: 7px var(--space-sm);
        background: var(--color-surface-2);
        border: 1px solid var(--color-hairline);
        border-radius: var(--radius-md);
        color: var(--color-ink-tertiary);
        cursor: pointer;
        transition: all var(--transition-fast);
    }

    .search-box:hover {
        border-color: var(--color-hairline-strong);
        color: var(--color-ink-subtle);
    }

    .search-placeholder {
        flex: 1;
        font-size: 13px;
    }

    .search-shortcut {
        display: flex;
        gap: 3px;
    }

    .search-shortcut kbd {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        min-width: 20px;
        height: 20px;
        padding: 0 5px;
        background: var(--color-surface-3);
        border: 1px solid var(--color-hairline);
        border-radius: var(--radius-xs);
        font-family: var(--font-text);
        font-size: 11px;
        font-weight: 500;
        color: var(--color-ink-subtle);
    }

    .topbar-actions {
        display: flex;
        align-items: center;
        gap: var(--space-xs);
    }

    @media (max-width: 768px) {
        .topbar {
            padding: 0 var(--space-md);
        }

        .search-shortcut {
            display: none;
        }

        .search-wrapper {
            max-width: none;
        }
    }
</style>
