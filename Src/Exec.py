from Src.Svr import SVR

'''
    Starting point of the program.
'''
def main():
    server = SVR()
    conn, addr = server.initiate()

    while True:
        in_data = conn.recv(1024)

        if not in_data:
            server.tearDown(conn)
            conn, addr = server.initiate()

        else:
            print(in_data.decode())
            output = input(">> ")
            conn.send(output.encode('ascii'))

main()


