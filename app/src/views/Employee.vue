<!--
@file app/src/views/Employee.vue

This component is used to render the view of an Employee
-->
<template>
    <v-app v-bind:id="id">

        <v-app-bar app color="indigo" dark>
            <v-btn icon v-bind:to="{name: 'admin', query: {tab: 'employees'}}">
                <v-icon>mdi-arrow-left</v-icon>
            </v-btn>

            <v-toolbar-title>{{ employee.name }}</v-toolbar-title>
            <v-spacer></v-spacer>

            <v-btn icon v-on:click.stop="open_edit_employee_dialog()">
                <v-icon>mdi-pencil</v-icon>
            </v-btn>

            <v-btn icon v-on:click.stop="open_delete_employee_dialog()">
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
                    <v-tab href="#timesheets">Timesheets</v-tab>
                    <v-tab href="#contracts">Contracts</v-tab>
                    <v-tabs-slider></v-tabs-slider>
                </v-tabs>
            </template>
        </v-app-bar>

        <v-content>
            <v-container fluid no-gutters class="pa-0">
                <v-tabs-items v-model="tab">
                    <v-tab-item value="timesheets">
                        <EmployeeTimesheetsList v-bind:employee_id="employee_id" />
                    </v-tab-item>
                    <v-tab-item value="contracts">
                        <EmployeeContractsList v-bind:employee_id="employee_id" />
                    </v-tab-item>
                </v-tabs-items>

                <v-fab-transition>
                    <v-btn color="pink" dark bottom right fab large fixed
                           :key="active_fab.name"
                           v-on:click.stop="fab_click()">
                        <v-icon>{{ active_fab.icon }}</v-icon>
                    </v-btn>
                </v-fab-transition>

                <CreateEmployeeTimesheetEntryForm v-bind:employee_id="employee_id"
                                                  v-bind:dialog="add_employee_timesheet_entry_dialog"
                                                  v-on:update-dialog="close_add_employee_timesheet_entry_dialog()" />

                <CreateEmployeeContractForm v-bind:employee_id="employee_id"
                                            v-bind:dialog="add_employee_contract_dialog"
                                            v-on:update-dialog="close_add_employee_contract_dialog()" />

                <EditEmployeeForm v-bind:employee="employee"
                                  v-bind:dialog="edit_employee_dialog"
                                  v-on:update-dialog="close_edit_employee_dialog()" />

                <DeleteEmployeeForm v-bind:employee="employee"
                                    v-bind:dialog="delete_employee_dialog"
                                    v-on:update-dialog="close_delete_employee_dialog()" />

            </v-container>
        </v-content>

    </v-app>
</template>

<script>
import EmployeeTimesheetsList from "../components/EmployeeTimesheetsList";
import EmployeeContractsList from "../components/EmployeeContractsList.vue";
import CreateEmployeeTimesheetEntryForm from "../components/CreateEmployeeTimesheetEntryForm";
import EditEmployeeForm from "../components/EditEmployeeForm";
import DeleteEmployeeForm from "../components/DeleteEmployeeForm";
import CreateEmployeeContractForm from "../components/CreateEmployeeContractForm";

export default {
    name: 'Employee',
    props: ['employee_id', 'initial_tab'],
    components: {
        CreateEmployeeContractForm,
        DeleteEmployeeForm,
        EditEmployeeForm,
        CreateEmployeeTimesheetEntryForm,
        EmployeeContractsList,
        EmployeeTimesheetsList
    },
    data: function () {
        return {
            id: 'employee',
            title: 'Employee',
            loading: false,

            tab: this.initial_tab,

            edit_employee_dialog: false,
            delete_employee_dialog: false,

            add_employee_contract_dialog: false,
            add_employee_timesheet_entry_dialog: false,
        }
    },
    computed: {
        employee() {
            let _employee = null;
            if (this.employee_id) {
                _employee = this.$store.getters['employees/employee'](this.employee_id);
            }
            return _employee;
        },
        active_fab() {
            switch(this.tab) {
                case 'timesheets':
                    return {name: 'timesheets', icon: 'mdi-calendar-clock'};
                case 'contracts':
                    return {name: 'contracts', icon: 'mdi-newspaper-plus'};
                default: {
                    return {};
                }
            }
        }
    },
    watch: {
        employee_id (new_employee_id) {
            if (new_employee_id) {
                this.initialize();
            }
        },
    },
    created () {
        this.initialize();
    },
    methods: {
        initialize() {
            if (this.employee_id) {
                this.loading = true;
                this.$store.dispatch('employees/get_employee', this.employee_id)
                    .then(() => {
                        this.loading = false;
                    });
            }
        },
        fab_click () {
            switch(this.tab) {
                case 'timesheets':
                    this.add_employee_timesheet_entry_dialog = true;
                    return;
                case 'contracts':
                    this.add_employee_contract_dialog = true;
                    return;
                default:
                    return;
            }
        },
        /**
         * Close the add Employee Timesheet Entry dialog
         */
        close_add_employee_timesheet_entry_dialog() {
            this.add_employee_timesheet_entry_dialog = false;
        },

        /**
         * Close the add Employee Contract dialog
         */
        close_add_employee_contract_dialog() {
            this.add_employee_contract_dialog = false;
        },

        /**
         * Open the edit Employee dialog
         */
        open_edit_employee_dialog () {
            this.edit_employee_dialog = true;
        },
        /**
         * Close the edit Employee dialog
         */
        close_edit_employee_dialog () {
            this.edit_employee_dialog = false;
        },
        /**
         * Open the delete Employee dialog
         */
        open_delete_employee_dialog () {
            this.delete_employee_dialog = true;
        },
        /**
         * Close the delete Employee dialog
         */
        close_delete_employee_dialog () {
            this.delete_employee_dialog = false;
        },
    },
};
</script>