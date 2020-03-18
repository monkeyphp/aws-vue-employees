<!--
@file app/src/views/Admin.vue

This component is used to render the Admin view.
The view contains tabs navigation to the top level admin resources.

- Employees
- Groups
- Activities
-->
<template>
    <v-app v-bind:id="id">
        <v-app-bar app color="indigo" dark>
            <v-toolbar-title>
                {{ title }}
            </v-toolbar-title>
            <v-spacer></v-spacer>
            <v-btn icon>
                <v-icon>mdi-magnify</v-icon>
            </v-btn>

            <v-menu left bottom>
                <template v-slot:activator="{ on }">
                    <v-btn icon v-on="on">
                        <v-icon>mdi-dots-vertical</v-icon>
                    </v-btn>
                </template>

                <v-list>
                    <v-list-item>
                        <v-list-item-title>Settings (home)</v-list-item-title>
                    </v-list-item>
                    <v-list-item>
                        <v-list-item-title>About (home)</v-list-item-title>
                    </v-list-item>
                </v-list>
            </v-menu>

            <template v-slot:extension>
                <v-tabs v-model="tab"
                        centered
                        grow
                        slider-color="white"
                        background-color="transparent">
                    <v-tab href="#employees">Employees</v-tab>
                    <v-tab href="#groups">Groups</v-tab>
                    <v-tab href="#activities">Activities</v-tab>
                    <v-tabs-slider></v-tabs-slider>
                </v-tabs>
            </template>

        </v-app-bar>

        <v-content>
            <v-container fluid no-gutters class="pa-0">
                <v-tabs-items v-model="tab">
                    <v-tab-item value="employees">
                        <EmployeesList />
                    </v-tab-item>
                    <v-tab-item value="groups">
                        <GroupsList />
                    </v-tab-item>
                    <v-tab-item value="activities">
                        <ActivitiesList />
                    </v-tab-item>
                </v-tabs-items>

                <v-fab-transition>
                    <v-btn color="pink" dark bottom right fab large fixed
                            :key="activeFab.name"
                            v-on:click.stop="fab_click()">
                        <v-icon>{{ activeFab.icon }}</v-icon>
                    </v-btn>
                </v-fab-transition>

                <CreateEmployeeDialog v-bind:dialog="create_employee_dialog"
                                    v-on:update-dialog="close_create_employee_dialog()"/>

                <CreateGroupDialog v-bind:dialog="create_group_dialog"
                                 v-on:update-dialog="close_create_group_dialog()" />

                <CreateActivityDialog v-bind:dialog="create_activity_dialog"
                                    v-on:update-dialog="close_create_activity_dialog()" />

            </v-container>
        </v-content>
    </v-app>

</template>

<script>

import CreateActivityDialog from "@/components/CreateActivityDialog";
import CreateGroupDialog from "@/components/CreateGroupDialog";
import CreateEmployeeDialog from "@/components/CreateEmployeeDialog";



import EmployeesList from '@/components/EmployeesList.vue'
import GroupsList from "@/components/GroupsList";
import ActivitiesList from "@/components/ActivitiesList";

export default {
    name: 'Admin',
    components: {
        CreateEmployeeDialog,
        CreateGroupDialog,
        CreateActivityDialog,
        EmployeesList,
        GroupsList,
        ActivitiesList,
    },
    props: ['initial_tab', ],
    data: function () {
        return {
            id: 'admin',
            title: 'TimeBox',
            tab: this.initial_tab,
            create_employee_dialog: false,

            create_group_dialog: false,
            create_activity_dialog: false,
        };
    },
    methods: {
        fab_click () {
            switch(this.tab) {
                case 'employees':
                    this.create_employee_dialog = true;
                    return;
                case 'groups':
                    this.create_group_dialog = true;
                    return;
                case 'activities':
                    this.create_activity_dialog = true;
                    return;
                default:
                    return;
            }
        },
        /**
         * Set the `create_employ_employee` value to false and close
         * the `CreateEmployeeDialog.
         */
        close_create_employee_dialog () {
            this.create_employee_dialog = false;
        },
        /**
         * Set the `create_group_dialog` value to false and close the
         * `CreateGroupDialog`
         */
        close_create_group_dialog () {
            this.create_group_dialog = false;
        },
        /**
         * Set the `create_activity_dialog` value to false and
         * close the `CreateActivityDialog`.
         */
        close_create_activity_dialog () {
            this.create_activity_dialog = false;
        },
    },
    computed: {
        activeFab() {
            switch(this.tab) {
                case 'employees':
                    return {name: 'employees', icon: 'mdi-account-plus'};
                case 'groups':
                    return {name: 'groups', icon: 'mdi-account-multiple-plus'};
                case 'activities':
                    return {name: 'activities', icon: 'mdi-clipboard-list-outline'};
                default: {
                    return {};
                }
            }
        }
    }
};
</script>