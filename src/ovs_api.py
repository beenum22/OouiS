import socket
import json
import sys
import logging
import uuid


logger = logging.getLogger(__name__)


class OvsApi(object):
    """Simple API to interact with OVSDB"""

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.dbs = None
        try:
            self.connect_ovs()
        except Exception as err:
            logger.error("Failed to connect to the OvS server")
            logger.debug(err)
            logger.error("Exiting...")
            sys.exit(1)

    def connect_ovs(self):
        try:
            logger.debug("Connecting to the OvS Server on '%s':%s" %
                         (self.ip, self.port))
            self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.soc.connect((self.ip, self.port))
            logger.info("Connected to the OvS Server.")
        except socket.error as err:
            raise err

    def disconnect_ovs(self):
        try:
            logger.debug("Disconnecting from the OvS Server on '%s':%s" %
                         (self.ip, self.port))
            self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.soc.close()
            logger.info("Disconnected from the OvS Server.")
        except socket.error as err:
            raise err

    def send_rpc(self, call):
        try:
            logger.debug("Send the JSON RPC request: %s" % call)
            self.soc.send(json.dumps(call))
            #data_list = []
            '''
            while True:
                data = client_socket.recv(4096).decode('utf8')
                data_list.append(data)
                if not data:
                    break
            '''
            resp = self.soc.recv(8192).decode('utf8')
            logger.debug("Received the JSON RPC response: %s" % resp)
            #logger.debug("Received the JSON RPC response: %s" % ''.join(data_list))
            return resp
        except socket.error as err:
            raise err

    def get_schema(self):
        get_schema = {"method": "get_schema",
                      "params": ["Open_vSwitch"], "id": 0}
        try:
            resp = self.send_rpc(get_schema)
            return resp
        except Exception as err:
            logger.error("Error occurred sending an RPC call.")
            logger.error(err)
            logger.error("Exiting...")
            sys.exit(1)

    def monitor_ovs(self):
        monitor_json = {
            "method": "monitor",
            "id": 0,
            "params": ["Open_vSwitch",
                       None,
                       {
                           "Port": {
                               "columns": ["external_ids",
                                           "interfaces",
                                           "name",
                                           "tag",
                                           "trunks"]
                           },
                           "Controller": {
                               "columns": ["is_connected",
                                           "target"]
                           },
                           "Interface": {
                               "columns": ["name",
                                           "options",
                                           "type"]
                           },
                           "Open_vSwitch": {
                               "columns": ["bridges",
                                           "cur_cfg",
                                           "manager_options",
                                           "ovs_version"]
                           },
                           "Manager": {
                               "columns": ["is_connected",
                                           "target"]
                           },
                           "Bridge": {
                               "columns": ["controller",
                                           "name",
                                           "ports"]
                           }
                       }]
        }
        try:
            resp = self.send_rpc(monitor_json)
            return resp
        except Exception as err:
            logger.error("Error occurred sending an RPC call.")
            logger.error(err)
            logger.error("Exiting...")
            sys.exit(1)

    def get_dbs(self):
        try:
            list_dbs_query = {"method": "list_dbs", "params": [], "id": 0}
            resp = self.send_rpc(list_dbs_query)
            self.dbs = json.loads(resp)['result']
            return self.dbs
        except Exception as err:
            pass
            # logger.error(err)
            # logger.error("Exiting...")
            # sys.exit(1)

    def get_all_info(self):
        info = {
            "method": "monitor_cond",
            "params": [
                "Open_vSwitch",
                str(uuid.uuid4()),
                {
                    "Port": {
                        "columns": [
                            "fake_bridge",
                            "interfaces",
                            "name",
                            "tag"
                        ]
                    },
                    "Interface": {
                        "columns": [
                            "error",
                            "name",
                            "ofport",
                            "mac_in_use",
                            "type"
                        ]
                    },
                    "Controller": {
                        "columns": [

                        ]
                    },
                    "Bridge": {
                        "columns": [
                            "controller",
                            "fail_mode",
                            "name",
                            "ports"
                        ]
                    },
                    "Open_vSwitch": {
                        "columns": [
                            "bridges",
                            "cur_cfg"
                        ]
                    }
                }
            ],
            "id": 1
        }
        try:
            resp = self.send_rpc(info)
            return resp
        except Exception as err:
            #logger.error("Failed to fetch the OpenvSwitch topology info.")
            raise err

    def get_bridges(self):
        try:
            br_list = []
            data = json.loads(self.get_all_info())['result']['Bridge']
            for br in data.keys():
                br_list.append(data[br]['initial']['name'])
            return br_list
        except Exception as err:
            logger.debug(err)
            logger.error("Failed to fetch the list of bridges.")

    def get_br_ports(self, bridge):
        try:
            ports_list = []
            data = json.loads(self.get_all_info())['result']['Bridge']
            br_uuid = data.keys()
            for br in br_uuid:
                if data[br]['initial']['name'] == bridge:
                    if 'set' in data[br]['initial']['ports']:
                        p_list = data[br]['initial']['ports'][1]
                        ports_list = [
                            item for sublist in p_list for item in sublist if item != 'uuid']
                    else:
                        ports_list = data[br]['initial']['ports']
                        ports_list.remove('uuid')
                    return ports_list
            logger.info("No bridge: %s found." % bridge)
            return port_list
        except Exception as err:
            logger.debug(err)
            logger.error("Failed to fetch the list of ports.")

    def get_port_details(self, port_uuid):
        try:
            data = json.loads(self.get_all_info())['result']['Port']
            return data[port_uuid]['initial']
        except KeyError as err:
            logger.debug(KeyError(err))
            logger.error("Failed to fetch the port '%s' info." % port_uuid)
            raise

    def get_interface_details(self, iface_uuid):
        try:
            data = json.loads(self.get_all_info())['result']['Interface']
            return data[port_uuid]['initial']
        except KeyError as err:
            logger.debug(KeyError(err))
            logger.error("Failed to fetch the interface '%s' info." % iface_uuid)
            raise
        except:
            logger.error("Failed to fetch the interface '%s' info." % iface_uuid)
            raise
