import module2

def main():
    logger = logging.getLogger()
    logger.warning('Watch out!')  # will print a message to the console
    logger.info('I told you so')
    module2.foo()

if __name__ == '__main__':
   
    main()
    
