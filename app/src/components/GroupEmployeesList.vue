<!--
@file app/src/components/GroupEmployeesList.vue

This component is used to render a list of the Employees that have been added to the
specified Group.
-->
<template>
    <v-list two-line class="pa-0">
        <template v-for="(item, index) in group_employees">
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
    name: 'GroupEmployeesList',
    props: ['group_id'],
    watch: {
        group_id (new_group_id) {
            if (new_group_id) {
                this.initialize();
            }
        }
    },
    created () {
        this.initialize();
    },
    computed: {
        group_employees () {
            return this.$store.getters['employees/employees'](this.group_id)
        }
    },
    methods: {
        initialize () {
            this.loading = true;
            this.$store.dispatch('employees/get_employees', this.group_id)
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
    }
};
</script>