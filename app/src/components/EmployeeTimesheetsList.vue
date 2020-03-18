<!--
This component is used to render a list of the Timeshetes for the Employee
/* eslint-disable */
-->
<template>

    <v-list two-line subheader class="py-0">

        <template v-for="(value, name) in employee_timesheets">
            <v-subheader v-bind:key="name">{{ name }}</v-subheader>

            <template v-for="(item, index) in value">
                <v-list-item v-bind:key="item.date"
                             :to="{ name: 'employee-timesheet', params: { employee_id: item.employee_id, date: item.date}}">
                    <v-list-item-content>
                        <v-list-item-title>{{ item.date }}</v-list-item-title>
                        <v-list-item-subtitle>{{ item.total / 60 }} hrs</v-list-item-subtitle>
                    </v-list-item-content>
                </v-list-item>
                <v-divider v-bind:key="index" />
            </template>
        </template>
    </v-list>

</template>

<script>
/* eslint-disable */
export default {
    name: 'EmployeeTimesheetsList',
    props: ['employee_id'],
    watch: {
        employee_id (new_employee_id) {
            if (new_employee_id) {
                this.initialize();
            }
        },
    },
    computed: {
        employee () {
            let _employee = null;
            if (this.employee_id) {
                _employee = this.$store.getters['employees/employee'](this.employee_id);
            }
            return _employee;
        },
        employee_timesheets () {
            let _employee_timesheets = {};
            if (this.employee_id) {
                _employee_timesheets = this.$store.getters['employees/employee_timesheets'](this.employee_id);

                const sorted = {};
                _employee_timesheets.forEach((timesheet) => {
                    let y = timesheet.year;
                    let m = timesheet.month;

                    let subheader = `${m} ${y}`;

                    if (! sorted.hasOwnProperty(subheader)) {
                        sorted[subheader] = [];
                    }
                    sorted[subheader].push(timesheet);
                });
                _employee_timesheets = sorted;
            }
            return _employee_timesheets;
        },
    },
    created () {
        this.initialize();
    },
    methods: {
        initialize() {
            if (this.employee_id) {
                this.loading = true;
                this.$store.dispatch('employees/get_employee_timesheets', this.employee_id)
                    .then(() => { this.loading = false;})
            }
        },
    },
    data: function () {
        return {
            title: 'Timesheets',
            loading: false,
            loading_text: "Loading Employee Timesheets... please wait",
        };
    },
}
</script>