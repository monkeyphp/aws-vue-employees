<!--
@file app/src/views/EmployeeContract.vue

This component is used to render the specified Contract.
-->
<template>
    <v-app v-bind:id="id">
        <v-app-bar app color="indigo" dark>
            <v-btn icon exact v-bind:to="{name: 'employee', params: {employee_id: employee_id}, query: {tab: 'contracts'}}">
                <v-icon>mdi-arrow-left</v-icon>
            </v-btn>

            <v-toolbar-title>{{ employee_contract.start_date }}</v-toolbar-title>
            <v-spacer></v-spacer>

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

                <v-list>
                    <v-list-item two-line>
                        <v-list-item-content>
                            <v-list-item-title>Start Date</v-list-item-title>
                            <v-list-item-subtitle>{{ employee_contract.start_date }}</v-list-item-subtitle>
                        </v-list-item-content>
                    </v-list-item>

                    <v-list-item two-line>
                        <v-list-item-content>
                            <v-list-item-title>Weekly Hours</v-list-item-title>
                            <v-list-item-subtitle>{{ employee_contract.weekly_hours }}</v-list-item-subtitle>
                        </v-list-item-content>
                    </v-list-item>

                    <v-list-item two-line>
                        <v-list-item-content>
                            <v-list-item-title>Hourly Rate</v-list-item-title>
                            <v-list-item-subtitle>{{ employee_contract.hourly_rate }}</v-list-item-subtitle>
                        </v-list-item-content>
                    </v-list-item>
                </v-list>

            </v-container>
        </v-content>

    </v-app>
</template>

<script>
export default {
    name: 'EmployeeContract',
    props: ['employee_id', 'start_date'],
    watch: {
        employee_id (new_employee_id) {
            if (new_employee_id) {
                this.initialize();
            }
        },
        start_date (new_start_date) {
            if (new_start_date) {
                this.initialize();
            }
        }
    },
    computed: {
        employee_contract () {
            let _employee_contract;
            if (this.employee_id && this.start_date) {
                _employee_contract = this.$store.getters['employees/employee_contract']({'employee_id': this.employee_id, 'start_date': this.start_date});
            }
            return _employee_contract;
        },
    },
    created () {
        this.initialize();
    },
    methods: {
        initialize () {
            this.loading = true;
            this.$store.dispatch('employees/get_employee_contract', {'employee_id': this.employee_id, 'start_date': this.start_date})
                .finally(() => {
                    this.loading = false;
                })
        },
    },
    data: function () {
        return {
            id: 'employee-contract',
            loading: false,
            loading_text: 'Loading Contract... please wait',

        };
    }
};
</script>
