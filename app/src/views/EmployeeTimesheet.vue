<!--
This component is used to render the Employee Timesheet.
-->
<template>
    <v-app v-bind:id="id">
        <v-app-bar app color="indigo" dark>
            <v-btn icon exact v-bind:to="{name: 'employee', params: {employee_id: employee_id}, query: {tab: 'timesheets' }}">
                <v-icon>mdi-arrow-left</v-icon>
            </v-btn>

            <v-toolbar-title>{{ employee_timesheet.date }}</v-toolbar-title>
            <v-spacer></v-spacer>

            <v-btn icon v-on:click.stop="open_delete_employee_timesheet_dialog()">
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
        </v-app-bar>

        <v-content>
            <v-container fluid no-gutters class="pa-0">

                <v-list dense class="blue-grey lighten-5">
                    <v-list-item dense>
                        <v-list-item-content>
                            <v-list-item-title>Total Hours</v-list-item-title>
                        </v-list-item-content>
                        <v-list-item-action>
                            <v-list-item-action-text>{{ employee_timesheet.total / 60 }} hrs</v-list-item-action-text>
                        </v-list-item-action>
                    </v-list-item>
                </v-list>

                <v-list two-line subheader class="py-0">

                    <template v-for="(item, name, index) in employee_timesheet.entries">
                        <!--{{ name }} - {{ index }}-->

                        <v-list-item v-bind:key="item.start" v-on:click.stop="open_edit_employee_timesheet_entry(item)">
                            <v-list-item-content>
                                <v-list-item-title>{{ item.start }} to {{ item.finish }}</v-list-item-title>
                                <v-list-item-subtitle>{{ item.activity_id }}</v-list-item-subtitle>
                            </v-list-item-content>
                            <v-list-item-action>
                                <v-list-item-action-text>
                                    {{ item.duration }}
                                </v-list-item-action-text>
                            </v-list-item-action>
                        </v-list-item>
                        <v-divider v-bind:key="index" />
                    </template>
                </v-list>

                <!--<EmployeeTimesheetEntriesList v-bind:employee_id="employee_id"-->
                                              <!--v-bind:date="date"-->
                                              <!--v-on:edit-employee-timesheet-entry="open_edit_employee_timesheet_entry"/>-->
                <v-fab-transition>
                    <v-btn color="pink" dark bottom right fab large fixed
                           v-on:click.stop="open_create_timesheet_entry_dialog()">
                        <v-icon>mdi-calendar-clock</v-icon>
                    </v-btn>
                </v-fab-transition>

                <DeleteEmployeeTimesheetForm v-bind:employee_timesheet="employee_timesheet"
                                             v-bind:dialog="delete_employee_timesheet_dialog"
                                             v-on:update-dialog="close_delete_employee_timesheet_dialog()"/>

                <CreateEmployeeTimesheetEntryForm
                        v-bind:employee_id="employee_id"
                        v-bind:dialog="create_timesheet_entry_dialog"
                        v-on:update-dialog="close_create_timesheet_entry_dialog()" />


                <EditEmployeeTimesheetEntryForm
                        v-bind:entry="entry"
                        v-bind:dialog="edit_timesheet_entry_dialog"
                        v-on:update-dialog="close_edit_timesheet_entry_dialog()" />

            </v-container>
        </v-content>
    </v-app>
</template>

<script>
/* eslint-disable */
import EmployeeTimesheetEntriesList from '@/components/EmployeeTimesheetEntriesList.vue';
import CreateEmployeeTimesheetEntryForm from '@/components/CreateEmployeeTimesheetEntryForm.vue';
import EditEmployeeTimesheetEntryForm from '@/components/EditEmployeeTimesheetEntryForm.vue';
import DeleteEmployeeTimesheetForm from '@/components/DeleteEmployeeTimesheetForm.vue';

export default {
    name: 'EmployeeTimesheet',
    props: ['employee_id', 'date'],
    components: {
        EmployeeTimesheetEntriesList,
        CreateEmployeeTimesheetEntryForm,
        EditEmployeeTimesheetEntryForm,
        DeleteEmployeeTimesheetForm
    },
    data: function () {
        return {
            id: 'employee-timesheet',
            title: 'Employee Timesheet',
            loading: false,
            create_timesheet_entry_dialog: false,
            edit_timesheet_entry_dialog: false,
            delete_employee_timesheet_dialog: false,
            entry: null,
        };
    },
    watch: {
        employee_id (new_employee_id) {
            this.initialize();
        },
        date (new_date) {
            this.initialize();
        },
    },
    computed: {
        employee() {
            let _employee = null;
            if (this.employee_id) {
                _employee = this.$store.getters['employees/employee'](this.employee_id);
            }
            return _employee;
        },
        employee_timesheet () {
            let _employee_timesheet = null;
            if (this.employee_id) {
                _employee_timesheet = this.$store.getters['employees/employee_timesheet']({'employee_id': this.employee_id, 'date': this.date})
            }

            return _employee_timesheet;
        },
    },
    created () {
        this.initialize();
    },
    filters: {
        date_format: function (value) {
            // const date = new Date(value);
            // return HH:MM
            return new Date(Date.parse(value)).toLocaleDateString('en-GB', {timeStyle: 'short'});
        },

        capitalize: function (value) {
            if (!value) return ''
            value = value.toString()
            return value.charAt(0).toUpperCase() + value.slice(1)
        }
    },
    methods: {
        initialize() {
            this.loading = true;
            this.$store.dispatch('employees/get_employee', this.employee_id)
                .then(() => {
                    this.loading = false;
                });

            this.loading = true;
            this.$store.dispatch('employees/get_employee_timesheet', {'employee_id': this.employee_id, 'date': this.date})
                .then(() => {
                    this.loading = false;
                });
        },
        /**
         * Open the delete Employee Timesheet Dialog
         */
        open_delete_employee_timesheet_dialog () {
            this.delete_employee_timesheet_dialog = true;
        },

        /**
         * Close the delete Employee Timesheet Dialog
         */
        close_delete_employee_timesheet_dialog () {
            this.delete_employee_timesheet_dialog = false;
        },

        /**
         *
         */
        open_create_timesheet_entry_dialog () {
            this.create_timesheet_entry_dialog = true;
        },
        /**
         *
         */
        close_create_timesheet_entry_dialog () {
            this.create_timesheet_entry_dialog = false;
        },
        /**
         * Function used to handle a timesheet entry being clicked
         *
         * @param entry
         */
        open_edit_employee_timesheet_entry (entry) {
            console.log(entry);
            this.entry = entry;
            this.edit_timesheet_entry_dialog = true;
        },
        /**
         *
         */
        close_edit_timesheet_entry_dialog () {
            this.edit_timesheet_entry_dialog = false;
            this.entry = null;
        }
    },
}
</script>