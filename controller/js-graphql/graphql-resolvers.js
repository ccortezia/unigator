var sql = require('yesql')('./sql/', {type: 'pg'});

module.exports = {};

module.exports.resolvers = {
    Query: {
        contact: (root, args, context, info) => {
            return { id: args.id, name: 'Mancey' };
        },
        contacts: (root, args, context, info) => {
            return [];
        },
        location: (root, args, context, info) => {
            return { id: args.id, addr_1: 'Sala 12' };
        },
        locations: (root, args, context, info) => {
            return [];
        },
        vehicle: (root, args, context, info) => {
            return null;
        },
        vehicles: (root, args, context, info) => {
            return [];
        },
        checkpoint: (root, args, context, info) => {
            return null;
        },
        checkpoints: (root, args, context, info) => {
            return [];
        },
        accessRule: (root, args, context, info) => {
            return null;
        },
        accessRules: (root, args, context, info) => {
            return [];
        },
        accessProc: (root, args, context, info) => {
            return null;
        },
        accessProcsHistory: (root, args, context, info) => {
            return [];
        },
        accessProcsRunning: (root, args, context, info) => {
            return [];
        },
        accessAuth: (root, args, context, info) => {
            return context.db.query(sql.getMatchingRuleForAccessEvent({
                ctc: args.info.contactId,
                vhc: args.info.vehicleId,
                ckp: args.info.checkpointId,
                orig: args.info.origLocationId,
                dest: args.info.destLocationId,
                ts: args.info.datetime
            }))
                .then(result => {
                    if (result.rowCount != 1) {
                        return null;
                    }
                    var row = result.rows[0];
                    return {
                        rule_id: row.rule_id,
                        auth_action: {
                            name: row.auth_name,
                            level: row.auth_level
                        }
                    };
                });
        }
    }
};
