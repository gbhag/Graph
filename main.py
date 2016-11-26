import pcap_parser
import graph_builder
import tshark
import argparse
import os
import glob


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-w ', '--write ', help="Absolute path of the new PCAP files to"
                        "be created", action="store", dest="write_file")
    parser.add_argument('-r ', '--read ', help="Give the absolute path to the"
                        "folder containing a pcap file(s). Reads the pcap file"
                        " and build a visual representation of it",
                        action="store", dest="read_file")
    args = parser.parse_args()

    if args.write_file:
        try:
            tshark.traffic_capture(args.write_file)
        except KeyboardInterrupt:
            for pcap_file in os.listdir(args.write_file):
                graph_builder.build_graph(pcap_parser.complete_view(pcap_file),
                                          '%s_complete_view' % pcap_file)
                graph_builder.build_graph(pcap_parser.red_team(pcap_file),
                                          '%s_red_team' % pcap_file)
                graph_builder.build_graph(pcap_parser.scorebot(pcap_file),
                                          '%s_scorebot' % pcap_file)
                graph_builder.build_graph(pcap_parser.file_transfer(pcap_file)
                                          , '%s_file_transfer' % pcap_file)

    elif args.read_file:
        # in order to provide a clear visualization I had to
        # use editcap to cute the overall pcap files into smaller
        # chunks. This functon reads each of the smaller pcap files
        # and builds four graphs from them.
        for pcap_file in glob.glob(os.path.join(args.read_file, '*.pcap')):
            graph_builder.build_graph(pcap_parser.complete_view(pcap_file), '%s_complete_view' % os.path.basename(pcap_file[:-5]))
            graph_builder.build_graph(pcap_parser.red_team(pcap_file), '%s_red_team' % os.path.basename(pcap_file[:-5]))
            graph_builder.build_graph(pcap_parser.scorebot(pcap_file), '%s_scorebot' % os.path.basename(pcap_file[:-5]))
            graph_builder.build_graph(pcap_parser.file_transfer(pcap_file), '%s_file_transfer' % os.path.basename(pcap_file[:-5]))

if __name__ == '__main__':
    main()
