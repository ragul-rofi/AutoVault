<script lang="ts">
    import { user } from './lib/authStore';
    import { theme } from './lib/design/themeStore';
    import Login from './lib/Login.svelte';
    import Dashboard from './lib/Dashboard.svelte';

    // Initialize theme on mount
    $: if ($theme) {
        document.documentElement.setAttribute('data-theme', $theme);
    }
</script>

<main>
    {#if $user}
        <Dashboard />
    {:else}
        <Login />
    {/if}
</main>
