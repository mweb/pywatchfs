#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (C) 2012 Mathias Weber <mathew.weber@gmail.com>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#   * Redistributions of source code must retain the above copyright notice,
#     this list of conditions and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions and the following disclaimer in the documentation
#     and/or other materials provided with the distribution.
#   * Neither the name of Pioneers of the Inevitable, Songbird, nor the names
#     of its contributors may be used to endorse or promote products derived
#     from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#

import os
import argparse
import pyinotify

__VERSION__ = "0.0"


class CloseProcessor(pyinotify.ProcessEvent):
    def process_default(self, event):
        f = event.name and os.path.join(event.path, event.name) or event.path
        print '> {0}'.format(f)


def monitor_directory(path):
    ''' Monitor the given directory for all file access to see which files are
        used.

        @param: The path to observer
    '''
    wmanager = pyinotify.WatchManager()
    notifier = pyinotify.Notifier(wmanager, CloseProcessor())
    wmanager.add_watch(path, pyinotify.EventsCodes.OP_FLAGS['IN_ACCESS'] |
            pyinotify.EventsCodes.OP_FLAGS['IN_ATTRIB'],
            rec=True)

    try:
        while 1:
            notifier.process_events()
            if notifier.check_events():
                notifier.read_events()
    except KeyboardInterrupt:
        notifier.stop()
        return


def main():
    ''' The main method do the argmuent parsing and call the listener. '''
    parser = argparse.ArgumentParser(description="Listen on a directory for "
            "all kind of file access.")
    parser.add_argument('--verbose', '-v', action='count',
            help="enable verbose output")
    parser.add_argument('--version', action='version', version='%(prog)s '
            '{0}'.format(__VERSION__))
    parser.add_argument('--output', '-o', help="Use the given file as output "
            "instead of the stdout")
    parser.add_argument('path', help='The directory to observer', type=str)

    args = parser.parse_args()
    monitor_directory(args.path)

if __name__ == '__main__':
    main()
