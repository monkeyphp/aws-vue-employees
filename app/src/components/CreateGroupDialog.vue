<!--
@file app/src/components/CreateGroupDialog.vue
This component is used to render a form for adding an Group.
-->
<template>
    <v-dialog v-model="_dialog" fullscreen hide-overlay transition="dialog-bottom-transition">
        <v-card v-bind:loading="loading" class="d-flex flex-column" tile>

            <v-toolbar dark color="indigo" class="flex-grow-0">
                <v-btn icon dark v-on:click="_dialog = false"><v-icon>mdi-close</v-icon></v-btn>
                <v-toolbar-title>{{ title }}</v-toolbar-title>
            </v-toolbar>

            <v-card-text class="flex-grow-1 pt-5">
                <v-form v-model="valid" ref="form" lazy-evaluation>
                    <v-text-field v-model="name"
                                  v-bind:rules="name_rules"
                                  required
                                  v-bind:counter="name_counter"
                                  label="Name" name="name" type="text"
                                  hint="The Group Name"></v-text-field>

                    <v-text-field v-model="group_id"
                                  v-bind:rules="group_id_rules"
                                  v-bind:counter="group_id_counter"
                                  label="Group Id" name="group_id" type="text"
                                  hint="The Group Id"></v-text-field>

                    <v-select v-model="parent_group_id"
                              v-bind:items="parent_groups"
                              v-bind:rules="parent_group_id_rules"
                              item-text="name"
                              item-value="group_id"
                              label="Parent Group" name="parent_group_id"/>

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
    /* eslint-disable */
export default {
    name: 'CreateGroupDialog',
    props: ['dialog'],
    data: function () {
        return {
            loading: false,
            title: 'Create Group',
            valid: false,

            name: null,
            name_counter: 25,
            name_rules: [
                name => !!name || "A name is required",
            ],

            group_id: null,
            group_id_counter: 25,
            group_id_rules: [
                // employee_group_id => !!employee_group_id || "An Group Id is required",
            ],

            parent_group_id: null,
            parent_group_id_rules: [
                parent_group_id => !! parent_group_id || "A Parent Group is required",
            ],
        };
    },
    created() {
        this.initialize();
    },
    computed: {
        parent_groups() {
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
    methods: {
        initialize() {
            this.loading = true;
            this.$store.dispatch('groups/get_groups')
                .finally(() => {
                    this.loading = false;
                });
        },
        cancel() {
            this.reset();
            this.close();
        },
        submit() {
            if (this.$refs.form.validate()) {
                this.loading = true;
                this.$store.dispatch('groups/post_group', {
                    name: this.name,
                    group_id: this.group_id,
                    parent_group_id: this.parent_group_id,
                }).then(() => {
                    this.loading = false;
                    this.close();
                    this.reset();
                }).catch((error) => {
                    this.loading = false;
                    if (error.hasOwnProperty('message')) {
                        console.log(error.message);

                    }
                    this.cancel();
                });
            }
        },
        close() {
            this.$emit('update-dialog', false);
        },
        reset() {
            this.name = null;
            this.group_id = null;
            this.parent_group_id = null;

            this.$refs.form.reset();
            this.$refs.form.resetValidation();
        },
    }
}
</script>