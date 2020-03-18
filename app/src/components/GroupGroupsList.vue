<!--
@file app/src/components/GroupGroupsList.vue

This component is used to render a list of the (sub) Groups that have been added to the
specified Group.
-->
<template>
    <v-list two-line class="py-0">
        <template v-for="(item, index) in group_groups">
            <v-list-item v-bind:key="item.group_id" exact
                         :to="{ name: 'group', params: { group_id: item.group_id}}">
                <v-list-item-avatar>
                    <v-avatar :color="item.color ? item.color : 'indigo'" size="36">
                        <span class="white--text">{{ item.initials ? item.initials : 'ZZ'}}</span>
                    </v-avatar>
                </v-list-item-avatar>
                <v-list-item-content>
                    <v-list-item-title v-html="item.name"></v-list-item-title>
                    <!-- @todo add number of members -->
                    <!--<v-list-item-subtitle v-html="item.group_id"></v-list-item-subtitle>-->
                </v-list-item-content>
            </v-list-item>
            <v-divider v-bind:key="index" />
        </template>
    </v-list>
</template>

<script>
export default {
    name: 'GroupGroupsList',
    props: ['group_id'],
    watch: {
        group_id (new_group_id) {
            if (new_group_id) {
                this.initialize();
            }
        }
    },

    computed: {
        group_groups () {
            return this.$store.getters['groups/group_groups'](this.group_id);
        },
    },
    created () {
        this.initialize();
    },
    methods: {
        initialize () {
            this.loading = true;
            this.$store.dispatch('groups/get_group_groups', this.group_id)
                .finally(() => {
                    this.loading = false;
                });
        },
    },
    data: function () {
        return {
            loading: false,
            loading_text: 'Loading Groups... please wait',
        };
    }
}
</script>