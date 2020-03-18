<!--
@file app/src/components/EmployeeContractsList.vue
This component is used to render a list of Contracts for the specified Employee.

employee_id: "1000"
start_date: "2020-01-01"
created: "2020-01-20 11:36:23.330509+00:00"
weekly_hours: "1000"
hourly_rate: "2000"
-->
<template>
    <v-list two-line class="py-0">
        <template v-for="(item, index) in employee_contracts">
            <v-list-item v-bind:key="item.start_date"
                         exact
                         :to="{ name: 'employee-contract', params: { employee_id: item.employee_id, start_date: item.start_date}}">
                <v-list-item-content>
                    <v-list-item-title>{{ item.start_date }}</v-list-item-title>
                    <v-list-item-subtitle>{{ item.weekly_hours }} hrs</v-list-item-subtitle>
                </v-list-item-content>
                <v-list-item-action>
                    <v-list-item-action-text>
                        {{ item.hourly_rate }}
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
    name: 'EmployeeContractsList',
    props: ['employee_id'],
    created() {
        this.initialize();
    },
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
        employee_contracts() {
            let _employee_contracts = [];
            if (this.employee_id) {
                _employee_contracts = this.$store.getters['employees/employee_contracts'](this.employee_id);
            }
            return _employee_contracts;
        },
    },
    methods: {
        // only run once
        initialize() {
            if (this.employee_id) {
                this.loading = true;
                this.$store.dispatch('employees/get_employee_contracts', this.employee_id)
                    .then(() => {
                        this.loading = false;
                    });
            }
        },
    },
    data: function () {
        return {
            loading: false,
            loading_text: "Loading Employee Contracts... please wait",
        };
    },
};
</script>