<!--
@file app/src/components/EditGroupForm.vue

This component is used to render a dialog for editing a Group.
-->
<template>
    <v-dialog v-model="_dialog" fullscreen hide-overlay transition="dialog-bottom-transition">
        <v-card v-bind:loading="loading" class="d-flex flex-column">

            <v-toolbar dark color="indigo" class="flex-grow-0">
                <v-btn icon dark v-on:click="cancel()"><v-icon>mdi-close</v-icon></v-btn>
                <v-toolbar-title>{{ title }}</v-toolbar-title>
            </v-toolbar>

            <v-card-text class="flex-grow-1 pt-5">
                <v-form v-model="valid" ref="form">
                    <v-text-field v-model="name"
                                  v-bind:rules="name_rules"
                                  v-bind:counter="name_counter"
                                  required
                                  label="Name" name="name" type="text" />

                    <v-text-field v-model="group_id"
                                  v-bind:rules="group_id_rules"
                                  readonly
                                  v-bind:counter="group_id_counter"
                                  label="Group Id" name="group_id" type="text" />

                    <v-select v-model="parent_group_id"
                              v-bind:items="parent_groups"
                              v-bind:rules="parent_group_id_rules"
                              item-text="name"
                              item-value="group_id"
                              label="Parent Group" name="parent_group_id" />
                </v-form>
            </v-card-text>

            <v-card-actions class="justify-center">
                <v-btn color="indigo" text  v-on:click="cancel()" class="flex-grow-1">Cancel</v-btn>
                <v-btn color="success" :loading="loading" v-on:click="submit()" class="flex-grow-1" v-bind:disabled="! valid">Save</v-btn>
            </v-card-actions>
        </v-card>

    </v-dialog>
</template>

<script>
export default {
    name: 'EditGroupForm',
    props: ['group', 'dialog'],
    watch: {
        group (new_group) {
            if (new_group) {
                this.initialize();
            }
        }
    },
    data: function () {
        return {
            loading: false,
            title: 'Edit Group',
            valid: false,

            group_id: null,
            group_id_counter: 25,
            group_id_rules: [
                group_id => !!group_id || "A Group Id is required",
            ],

            name: null,
            name_counter: 25,
            name_rules: [
                name => !!name || "A name is required",
            ],

            parent_group_id: null,
            parent_group_id_rules: [

            ],
        };
    },
    computed: {
        parent_groups () {
            return this.$store.getters['groups/groups'];
        },
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
            const name = this.group.name;
            const group_id = this.group.group_id;
            const parent_group_id = this.group.parent_group_id;

            this.name = name;
            this.group_id = group_id;
            this.parent_group_id = parent_group_id;
            this.title = `Edit ${name}`;
        },
        cancel() {
            this.close();
            this.reset();
        },
        submit() {
            if (this.$refs.form.validate()) {
                this.loading = true;
                this.$store.dispatch('groups/put_group', {
                    group_id: this.group_id,
                    parent_group_id: this.parent_group_id,
                    name: this.name,
                }).finally(() => {
                    this.loading = false;
                    this.close();
                    this.reset();
                });
            }
        },
        close() {
            this.$emit('update-dialog', false);
        },
        reset() {
            this.$refs.form.resetValidation();

            this.name = this.group.name;
            this.group_id = this.group.group_id;
            this.parent_group_id = this.group.parent_group_id;
        },
    },
}
</script>