<!--
This component is used to render a list of the Entries for the Timesheet.
-->
<template>
    <v-list two-line subheader class="py-0">
        <template v-for="(item, index) in employee_timesheet_entries">
            <v-list-item v-bind:key="item.start" v-on:click.stop="edit_employee_timesheet_entry(item)">
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
</template>

<script>
/* eslint-disable */
export default {
    name: 'EmployeeTimesheetEntriesList',
    props: ['employee_id', 'date'],
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
        employee_timesheet_entries() {
            let _employee_timesheet_entries = [];
            if (this.employee_id && this.date) {
                _employee_timesheet_entries = this.$store.getters['employees/employee_timesheet_entries']({'employee_id': this.employee_id, 'date': this.date})
            }
            return _employee_timesheet_entries;
        },
    },
    created () {
        this.initialize();
    },
    methods: {
        initialize() {
            this.loading = true;
            this.$store.dispatch('employees/get_employee_timesheet_entries', {'employee_id': this.employee_id, 'date': this.date})
                .then(() => {
                    this.loading = false;
                });
        },

        edit_employee_timesheet_entry (entry) {
            this.$emit('edit-employee-timesheet-entry', entry);
        },
    },
    data: function () {
        return {
            loading: false,
            loading_text: 'Loading Timesheet Entries... please wait',
        };
    },
}
</script>