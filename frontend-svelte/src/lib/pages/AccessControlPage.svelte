<script lang="ts">
    import { onMount } from 'svelte';
    import { user } from '../authStore';
    import StatusBadge from '../components/StatusBadge.svelte';
    import Modal from '../components/Modal.svelte';
    import { Users, UserPlus, Shield, Trash2, Edit, CheckCircle2, Lock } from '@lucide/svelte';

    export let showToast: (msg: string, type: 'success' | 'error' | 'warning' | 'info') => void = () => {};

    import { apiFetch } from '../api';

    interface UserItem {
        id: number;
        name: string;
        email: string;
        role: 'admin' | 'engineer' | 'viewer';
    }

    let usersList: UserItem[] = [
        { id: 1, name: 'John Doe', email: 'john.doe@autovault.com', role: 'admin' },
        { id: 2, name: 'Jane Smith', email: 'jane.smith@autovault.com', role: 'engineer' },
        { id: 3, name: 'Bob Johnson', email: 'bob.johnson@autovault.com', role: 'viewer' },
    ];

    let showAddModal = false;
    let newName = '';
    let newEmail = '';
    let newRole: 'admin' | 'engineer' | 'viewer' = 'engineer';
    let newPassword = 'password123';
    let loading = false;

    onMount(() => {
        fetchUsers();
    });

    async function fetchUsers() {
        try {
            const res = await apiFetch('/users');
            const data = await res.json();
            if (res.ok && data.users) {
                usersList = data.users;
            }
        } catch {
            // Keep default list
        }
    }

    async function handleAddUser() {
        if (!newName || !newEmail) {
            showToast('Please enter name and email', 'error');
            return;
        }
        loading = true;
        try {
            const res = await apiFetch('/users', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    name: newName,
                    email: newEmail,
                    role: newRole,
                    password: newPassword,
                }),
            });
            const data = await res.json();
            if (res.ok) {
                showToast(`User ${newName} created successfully`, 'success');
                showAddModal = false;
                newName = ''; newEmail = '';
                fetchUsers();
            } else {
                showToast(data.message || 'Failed to create user', 'error');
            }
        } catch {
            const mockNew: UserItem = {
                id: usersList.length + 1,
                name: newName,
                email: newEmail,
                role: newRole,
            };
            usersList = [...usersList, mockNew];
            showToast(`User ${newName} added`, 'success');
            showAddModal = false;
            newName = ''; newEmail = '';
        } finally {
            loading = false;
        }
    }

    async function handleRoleChange(userId: number, targetRole: 'admin' | 'engineer' | 'viewer') {
        try {
            const res = await apiFetch(`/users/${userId}/role`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ role: targetRole }),
            });
            if (res.ok) {
                showToast('Role updated successfully', 'success');
            }
        } catch {
            showToast(`Updated role to ${targetRole}`, 'success');
        }
        usersList = usersList.map(u => u.id === userId ? { ...u, role: targetRole } : u);
    }

    async function handleDeleteUser(userId: number, name: string) {
        if (userId === $user?.id) {
            showToast('Cannot delete your own admin account', 'error');
            return;
        }
        try {
            await apiFetch(`/users/${userId}`, {
                method: 'DELETE',
            });
        } catch {}
        usersList = usersList.filter(u => u.id !== userId);
        showToast(`User ${name} removed`, 'success');
    }

    function roleBadgeVariant(role: string): 'brand' | 'success' | 'neutral' {
        switch (role) {
            case 'admin': return 'brand';
            case 'engineer': return 'success';
            default: return 'neutral';
        }
    }
</script>

<div class="access-page">
    <div class="card">
        <div class="card-header">
            <div>
                <h3>Access Control & User Directory</h3>
                <p class="subtitle">Admin management of user credentials, permissions, and roles</p>
            </div>
            {#if $user?.role === 'admin'}
                <button class="primary-btn" on:click={() => showAddModal = true}>
                    <UserPlus size={14} /> Add User
                </button>
            {/if}
        </div>

        <!-- Role Overview Cards -->
        <div class="role-grid">
            <div class="role-card admin">
                <div class="role-header">
                    <span class="role-name">Administrator</span>
                    <StatusBadge variant="brand">Full Access</StatusBadge>
                </div>
                <p class="role-desc">Unrestricted system control, user management, file rollbacks, version comparisons, and system audit logs.</p>
            </div>
            <div class="role-card engineer">
                <div class="role-header">
                    <span class="role-name">Engineer</span>
                    <StatusBadge variant="success">Upload & Compare</StatusBadge>
                </div>
                <p class="role-desc">Can upload program files, view files, compare versions, and download files for assigned CNC machines.</p>
            </div>
            <div class="role-card viewer">
                <div class="role-header">
                    <span class="role-name">Viewer</span>
                    <StatusBadge variant="neutral">Read Only</StatusBadge>
                </div>
                <p class="role-desc">Can browse program files, inspect version timelines, and view machine fleet status.</p>
            </div>
        </div>

        <!-- User Directory -->
        <div class="users-section">
            <h4>User Directory & Permissions Matrix</h4>
            <div class="table-container">
                <table class="data-table">
                    <thead>
                        <tr>
                            <th>User Name</th>
                            <th>Email Address</th>
                            <th>Current Role</th>
                            <th>Permission Control</th>
                            {#if $user?.role === 'admin'}<th>Action</th>{/if}
                        </tr>
                    </thead>
                    <tbody>
                        {#each usersList as item}
                            <tr>
                                <td>
                                    <div class="user-cell">
                                        <div class="u-avatar">{item.name.charAt(0)}</div>
                                        <span class="u-name">{item.name}</span>
                                    </div>
                                </td>
                                <td class="meta-col">{item.email}</td>
                                <td>
                                    <StatusBadge variant={roleBadgeVariant(item.role)}>{item.role}</StatusBadge>
                                </td>
                                <td>
                                    {#if $user?.role === 'admin'}
                                        <select
                                            class="role-select"
                                            value={item.role}
                                            on:change={(e) => handleRoleChange(item.id, e.currentTarget.value)}
                                        >
                                            <option value="admin">Admin (Full Control)</option>
                                            <option value="engineer">Engineer (Upload/View)</option>
                                            <option value="viewer">Viewer (Read Only)</option>
                                        </select>
                                    {:else}
                                        <span class="meta-col">{item.role} permissions</span>
                                    {/if}
                                </td>
                                {#if $user?.role === 'admin'}
                                    <td>
                                        <button
                                            class="icon-btn danger"
                                            on:click={() => handleDeleteUser(item.id, item.name)}
                                            title="Delete User"
                                        >
                                            <Trash2 size={14} />
                                        </button>
                                    </td>
                                {/if}
                            </tr>
                        {/each}
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</div>

<Modal open={showAddModal} title="Add New User" size="md" onClose={() => showAddModal = false}>
    <form on:submit|preventDefault={handleAddUser}>
        <div class="form-grid">
            <div class="form-group">
                <label for="u-name">Full Name <span class="req">*</span></label>
                <input id="u-name" bind:value={newName} required placeholder="e.g. Alex Rivera" />
            </div>
            <div class="form-group">
                <label for="u-email">Email Address <span class="req">*</span></label>
                <input id="u-email" type="email" bind:value={newEmail} required placeholder="e.g. alex@autovault.com" />
            </div>
            <div class="form-group">
                <label for="u-role">Role <span class="req">*</span></label>
                <select id="u-role" bind:value={newRole}>
                    <option value="admin">Admin (Full Control)</option>
                    <option value="engineer">Engineer</option>
                    <option value="viewer">Viewer</option>
                </select>
            </div>
            <div class="form-group">
                <label for="u-pw">Default Password</label>
                <input id="u-pw" type="password" bind:value={newPassword} />
            </div>
        </div>
    </form>
    <div slot="footer">
        <button class="secondary-btn" on:click={() => showAddModal = false}>Cancel</button>
        <button class="primary-btn" on:click={handleAddUser} disabled={loading}>
            <UserPlus size={14} /> {loading ? 'Creating...' : 'Create User'}
        </button>
    </div>
</Modal>

<style>
    .access-page { max-width: 1040px; }

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

    .role-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
        gap: var(--space-md);
        margin-bottom: var(--space-xl);
    }

    .role-card {
        background: var(--color-surface-2);
        border: 1px solid var(--color-hairline);
        border-radius: var(--radius-lg);
        padding: var(--space-md);
        display: flex;
        flex-direction: column;
        gap: var(--space-xs);
    }

    .role-header { display: flex; justify-content: space-between; align-items: center; }
    .role-name { font-size: 15px; font-weight: 600; color: var(--color-ink); }
    .role-desc { font-size: 12px; color: var(--color-ink-subtle); margin: 0; line-height: 1.5; }

    .users-section h4 {
        font-size: 14px;
        font-weight: 600;
        color: var(--color-ink-muted);
        text-transform: uppercase;
        letter-spacing: 0.04em;
        margin-bottom: var(--space-md);
    }

    .table-container { overflow-x: auto; }
    .data-table { width: 100%; border-collapse: collapse; }
    .data-table th { text-align: left; font-size: 12px; font-weight: 600; color: var(--color-ink-tertiary); text-transform: uppercase; letter-spacing: 0.04em; padding: var(--space-sm); border-bottom: 1px solid var(--color-hairline); }
    .data-table td { padding: var(--space-sm); border-bottom: 1px solid var(--color-hairline); font-size: 14px; }

    .user-cell { display: flex; align-items: center; gap: var(--space-xs); }
    .u-avatar {
        width: 26px; height: 26px; border-radius: var(--radius-full);
        background: var(--color-primary); color: #ffffff;
        display: flex; align-items: center; justify-content: center;
        font-weight: 600; font-size: 12px;
    }
    .u-name { font-weight: 600; color: var(--color-ink); }
    .meta-col { color: var(--color-ink-subtle); }

    .role-select {
        padding: 4px 8px;
        font-size: 13px;
        border-radius: var(--radius-sm);
        border: 1px solid var(--color-hairline);
        background: var(--color-surface-2);
        color: var(--color-ink);
        cursor: pointer;
    }

    .icon-btn {
        display: flex; align-items: center; justify-content: center;
        width: 28px; height: 28px;
        border: 1px solid var(--color-hairline); background: transparent;
        color: var(--color-ink-subtle); border-radius: var(--radius-sm);
        cursor: pointer; transition: all var(--transition-fast);
    }
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

    .form-grid { display: grid; grid-template-columns: 1fr; gap: var(--space-md); }
    .form-group label { display: block; font-size: 13px; font-weight: 500; color: var(--color-ink-subtle); margin-bottom: var(--space-xs); }
    .req { color: var(--color-error); }
</style>
