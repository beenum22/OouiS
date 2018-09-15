#!/usr/bin/env python
# -*- coding: utf-8 -*-

__version__ = '1.0'
__author__ = 'beenum22'

import logging
import argparse
import sys
from src.ovs_api import OvsApi


logger = logging.getLogger('OouiS')
formatter = logging.Formatter(
    '[O-oui-S_v' + __version__ + '] %(levelname)s:%(asctime)s:%(message)s')
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)


class OouiS(object):

    def __init__(self):
        parser = argparse.ArgumentParser(
            description='OouiS', version=__version__)
        required_group = parser.add_argument_group('Required Parameters')
        optional_group = parser.add_argument_group('Optional Parameters')
        required_group.add_argument(
            '--ip', required=True, help='IP for the OvS server')
        required_group.add_argument(
            '--port', type=int, required=True, help='Port for the OvS server')
        optional_group.add_argument(
            "--debug", help="Add verbosity to the output", action="store_true")
        self.args = parser.parse_args()
        if self.args.debug:
            logger.setLevel(logging.DEBUG)
        else:
            logger.setLevel(logging.INFO)

    def run(self):
        try:
            print "---Bienvenue! Oui, Je suis OvS en français.---"
            api = OvsApi(self.args.ip, self.args.port)
            api.get_dbs()
            logger.info("OpenvSwitch DBs: %s" % api.dbs)
            # print api.monitor_ovs()
            # print api.get_schema()
            br_list = api.get_bridges()
            logger.info("OpenvSwitch Bridges: %s" % br_list)
            for br in br_list:
                p_list = api.get_br_ports(br)
                logger.info("Ports in Bridge '%s': %s" % (br, p_list))
            logger.info("Port: %s : %s" %
                        (p_list[0], api.get_port_details(p_list[0])))
            sample_port = api.get_port_details(p_list[0])
            logger.info("Interfaces in Port '%s': %s" % (
                p_list[0], sample_port['interfaces'][1]))
            exit()
            logger.info("Interface: %s : %s" % (
                p_list[0]['interfaces'][1], api.get_interface_details(p_list[0]['interfaces'][1])))
        except KeyError:
            logger.info("Oops!. Some key went wild!")
        except KeyboardInterrupt:
            api.disconnect_ovs()
            logger.info("Okay Okay, Calm down...")
            sys.exit(1)
        except Exception as err:
            logger.debug(err)
            logger.info("Oops!. Some key went wild!")
        finally:
            api.disconnect_ovs()
            logger.info("Testing Finished. Au revoir!")
            sys.exit(0)


def main():
    app = OouiS()
    app.run()


if __name__ == '__main__':
    main()
