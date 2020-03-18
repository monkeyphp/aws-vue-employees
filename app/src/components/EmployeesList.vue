<!--
@file app/src/components/EmployeesList.vue

This component is used to render a list of Employees currently in the application.
-->
<template>
    <v-list two-line class="pa-0">
        <template v-for="(item, index) in employees">
            <v-list-item v-bind:key="item.employee_id"
                         exact
                         :to="{ name: 'employee', params: { employee_id: item.employee_id}}">
                <v-list-item-avatar>
                    <v-avatar :color="item.color ? item.color : 'indigo'" size="36">
                        <span class="white--text">{{ item.initials ? item.initials : 'ZZ'}}</span>
                    </v-avatar>
                </v-list-item-avatar>
                <v-list-item-content>
                    <v-list-item-title v-html="item.name"></v-list-item-title>
                    <v-list-item-subtitle v-html="item.employee_id"></v-list-item-subtitle>
                </v-list-item-content>
            </v-list-item>
            <v-divider v-bind:key="index" />
        </template>
    </v-list>
</template>
<script>
export default {
    name: 'EmployeesList',
    computed: {
        employees () {
            return this.$store.getters['employees/employees']();
        },
    },
    created () {
        this.initialize();
    },
    methods: {
        initialize() {
            this.loading = true;
            this.$store.dispatch('employees/get_employees')
                .finally(() => {
                    this.loading = false;
                });
        },
    },
    data: function () {
        return {
            loading: false,
            loading_text: 'Loading Employees... please wait',
        };
    },
}
</script>
