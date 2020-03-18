<!--
@file app/src/components/DeleteEmployeeForm.vue

This component is used to render a dialog to confirm that the user wants
to delete the specified Employee.
-->
<template>
    <v-dialog v-model="_dialog" fullscreen hide-overlay transition="dialog-bottom-transition">
        <v-card v-bind:loading="loading" class="d-flex flex-column">
            <v-toolbar dark color="indigo" class="flex-grow-0">
                <v-btn icon dark v-on:click="cancel()">
                    <v-icon>mdi-close</v-icon>
                </v-btn>
                <v-toolbar-title>{{ title }}</v-toolbar-title>
            </v-toolbar>
            <v-card-text class="flex-grow-1 pt-5">
                <p>
                    Are you sure that you want to delete {{ name }}?
                </p>
            </v-card-text>

            <v-card-actions class="justify-center">
                <v-btn color="indigo" text  v-on:click="cancel()" class="flex-grow-1">Cancel</v-btn>
                <v-btn color="error" :loading="loading" v-on:click="confirm()" class="flex-grow-1">Delete</v-btn>
            </v-card-actions>
        </v-card>
    </v-dialog>
</template>

<script>
export default {
    name: 'DeleteEmployeeForm',
    props: ['employee', 'dialog'],
    watch: {
        employee (new_employee) {
            if (new_employee) {
                this.initialize()
            }
        }
    },
    data: function () {
        return {
            loading: false,
            title: 'Delete Employee',
            name: null,
        };
    },
    computed: {
        _dialog: {
            get: function () {
                return this.dialog;
            },
            set: function (val) {
                this.$emit('update-dialog', val);
            }
        },
    },
    created() {
        this.initialize();
    },
    methods: {
        initialize() {
            const name = this.employee.name;
            this.name = name;
            this.title = `Delete ${name}`;
        },
        cancel () {
            this.close();
            this.reset();
        },
        confirm () {
            this.loading = true;
            this.$store.dispatch('employees/delete_employee', this.employee)
                .finally(() => {
                    this.loading = false;
                    this.close();
                    this.$router.push({name: 'admin', query: {tab: 'employees'}});
                });
        },
        reset () {
            this.title = 'Delete Employee';
        },
        close () {
            this.$emit('update-dialog', false);
        },
    }
}
</script>