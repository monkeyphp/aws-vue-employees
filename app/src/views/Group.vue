<!--
@file app/src/views/Group.vue

This component is used to render a Group.
-->
<template>
    <v-app v-bind:id="id">

        <v-app-bar app color="indigo" dark>
            <v-btn icon v-bind:to="{name: 'admin', query: {tab: 'groups'}}">
                <v-icon>mdi-arrow-left</v-icon>
            </v-btn>

            <v-toolbar-title>{{ group.name }}</v-toolbar-title>
            <v-spacer></v-spacer>

            <v-btn icon v-on:click.stop="open_edit_group_dialog()">
                <v-icon>mdi-pencil</v-icon>
            </v-btn>

            <v-btn icon v-on:click.stop="open_delete_group_dialog()">
                <v-icon>mdi-delete</v-icon>
            </v-btn>

            <v-menu left bottom>
                <template v-slot:activator="{ on }">
                    <v-btn icon v-on="on">
                        <v-icon>mdi-dots-vertical</v-icon>
                    </v-btn>
                </template>
                <v-list>
                    <v-list-item>
                        <v-list-item-title>Settings</v-list-item-title>
                    </v-list-item>
                    <v-list-item>
                        <v-list-item-title>About</v-list-item-title>
                    </v-list-item>
                </v-list>
            </v-menu>

            <template v-slot:extension>
                <v-tabs v-model="tab"
                        centered
                        grow
                        slider-color="white"
                        background-color="transparent">
                    <v-tab href="#group-employees">Employees</v-tab>
                    <v-tab href="#group-groups">Groups</v-tab>
                    <v-tabs-slider></v-tabs-slider>
                </v-tabs>
            </template>


        </v-app-bar>

        <v-content>
            <v-container fluid no-gutters class="pa-0">

                <v-tabs-items v-model="tab">
                    <v-tab-item value="group-employees">
                        <GroupEmployeesList v-bind:group_id="group_id" />
                    </v-tab-item>
                    <v-tab-item value="group-groups">
                        <GroupGroupsList v-bind:group_id="group_id" />
                    </v-tab-item>
                </v-tabs-items>

                <EditGroupForm v-bind:group="group"
                               v-bind:dialog="edit_group_dialog"
                               v-on:update-dialog="close_edit_group_dialog()" />

                <DeleteGroupForm v-bind:group="group"
                                 v-bind:dialog="delete_group_dialog"
                                 v-on:update-dialog="close_delete_group_dialog()" />
            </v-container>
        </v-content>
    </v-app>
</template>

<script>
import GroupEmployeesList from '@/components/GroupEmployeesList.vue';
import GroupGroupsList from '@/components/GroupGroupsList.vue';
import EditGroupForm from '@/components/EditGroupForm';
import DeleteGroupForm from '@/components/DeleteGroupForm';

export default {
    name: 'Group',
    props: ['group_id'],
    components: {
        EditGroupForm,
        DeleteGroupForm,
        GroupEmployeesList,
        GroupGroupsList,
    },
    watch: {
        group_id (new_group_id) {
            if (new_group_id) {
                this.initialize();
            }
        },
    },
    created () {
        this.initialize();
    },
    computed: {
        group() {
            let _group = null;
            if (this.group_id) {
                _group = this.$store.getters['groups/group'](this.group_id);
            }
            return _group;
        }
    },
    methods: {
        initialize () {
            if (this.group_id) {
                this.loading = true;
                this.$store.dispatch('groups/get_group', this.group_id)
                    .finally(() => {
                        this.loading = false;
                    })
            }
        },

        open_edit_group_dialog () {
            this.edit_group_dialog = true;
        },

        close_edit_group_dialog () {
            this.edit_group_dialog = false;
        },

        open_delete_group_dialog () {
            this.delete_group_dialog = true;
        },

        close_delete_group_dialog () {
            this.delete_group_dialog = false;
        },
    },
    data: function () {
        return {
            id: 'group',
            title: 'Group',
            loading: false,
            loading_text: 'Loading Group... please wait',
            tab: null,
            edit_group_dialog: false,
            delete_group_dialog: false,
        };
    },
};
</script>