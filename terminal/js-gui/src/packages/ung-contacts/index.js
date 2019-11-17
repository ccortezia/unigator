import ContactsModule from './modules/ContactsModule';

export default {
    install(vv, opts = {namespace: '--'}) {
        vv.mixin({
            beforeMount() {
                this.$store.registerModule(opts.namespace, ContactsModule);
            },
        });
    }
};
