use std::net::{TcpListener, TcpStream};
use std::thread::{self, JoinHandle};
use std::sync::Mutex;
mod constants;
use crossbeam::scope;
use once_cell::sync::Lazy;
use hyper::Request;
use http::Request  as HttpRequest;
use local_ip_address;

#[cfg(test)]
mod tests {
    use std::{io::{Read, Write}, rc::Rc, sync::Arc, time::Duration, net::{IpAddr, Ipv4Addr}, string, ops::{Add, Deref}, env::args};

    use http::Error;

    use super::*;

    //static database: Mutex<P2pDatabase> = Mutex::new(P2pDatabase::new());\

    //deref -> lock -> unrwrap/match
    static DATABASE: Lazy<Arc<Mutex<P2pDatabase>>> =
        Lazy::new(|| Arc::new(Mutex::new(P2pDatabase::new())));
    #[test]

    /*
    let mut threads: Vec<JoinHandle<()>> = vec![];
        for i in 1..10 {
            let t = thread::spawn(move || {
                for j in 1..10 {
                    let s = format!("i: {}, j: {}", i, j);
                    
                    println!("{}", s);
                    let n = P2pNode {ip: s, thread_me: None};
                    let node_size: usize = std::mem::size_of::<P2pNode>();
                    unsafe {
                        database.connected_nodes.push(n);
                    }
                    thread::sleep(Duration::from_millis(100))
                }
            });
            threads.push(t);
            
        }

        for t in threads {
            t.join().unwrap()
        }

        unsafe { database.print_nodes() };
        assert_eq!("hello", "hello");
     */

    fn it_works() {

        let db = DATABASE.deref();
        
        //let listener1 = P2pListener::new( String::from("0.0.0.0:20000")).expect("msg");
        let listener2 = Arc::new(Mutex::new(P2pListener::new( String::from("0.0.0.0:20001")).expect("msg")));
        let list2_ref = listener2.clone(); 
        let t =thread::spawn(move || {
            list2_ref.lock().unwrap().listen_for_nodes();
        });
        
       let j =thread::spawn(|| {client_test()});
        j.join();
    }

    fn client_test(){
        println!("reached here");
        let mut new_socket = P2pListener::connect(String::from("127.0.0.1:20001")).expect("msg");
        println!("reached here 2");

        println!("reached here 3");
    }

    struct P2pDatabase {
        connected_nodes: Vec<P2pNode>
    }
    impl P2pDatabase {
        fn new() -> P2pDatabase {
            let connected_nodes: Vec<P2pNode> = Vec::new();
            P2pDatabase { connected_nodes: connected_nodes }
        }
        fn print_nodes(&self) {
            for node in self.connected_nodes.iter() {
                println!("{}", node.ip)
            }
        }
    }

    struct P2pListener {
        id: String,
        listener: TcpListener
    }

    impl P2pListener {
        fn new(addr: String) -> Result<P2pListener, std::io::Error> {
            let listener = match TcpListener::bind(&addr) {
                Ok(s) => s,
                Err(e) => {
                    return Err(e);
                }
            };

            Ok(P2pListener {listener: listener, id: addr.clone()})
        }

        fn connect(addr: String) -> Result<TcpStream, String>{
            let mut socket: TcpStream = match TcpStream::connect(addr) {
                Ok(s) => {
                    println!("sucessfully connected");
                    s
                }
                Err(e) => {
                    println!("could not connect to socket");
                    return Err(e.to_string())
                }
            }; 
            if P2pListener::client_handshake_protocol(&mut socket) {
                return Ok(socket);
            }
            return Err("could not connect to server".to_string());
            
        }
        fn listen_for_nodes(&self) {
            let listener: &TcpListener = &self.listener;
            println!("waiting for socket...");
            loop {
                let  (mut new_socket, socket_addr) = match listener.accept() {
                    Ok((s, a)) => {println!("found someone!"); s.set_read_timeout(Some(Duration::from_millis(1000))).expect("Could not set a read timeout");; (s, a)}
                    Err(e) => {
                        println!("error accepting socket: {}", e);
                        continue;
                    }
                };
                let mut ip_buffer = String::new();
                println!("server trying to read");
                
                let mut res: bool = false;
                //(new_socket, res) = P2pListener::validate_connection_server(new_socket);

                println!("why tf am i here");
                match P2pListener::server_handshake_protocol(&mut new_socket) {
                    Ok(ip) => {
                        ip_buffer = ip;
                    }
                    Err(e) => {println!("{}", e); continue;}
                };
                    
                match new_socket.read_to_string(&mut ip_buffer) {
                    Ok(_) => {println!("reading was successfull!, validating connection...");
                
                },
                    Err(_) => {
                        println!("error reading socket id... abandoning connection");
                        continue;} 

                };
                println!("{}", ip_buffer);
                let new_node = P2pNode::new(ip_buffer, new_socket);
                {
                    let db: &Arc<Mutex<P2pDatabase>> = DATABASE.deref();
                    let mut db = match db.lock() {
                        Ok(s) => s,
                        Err(e) => {println!("{}", e); continue;}
                        
                    }; 
                    db.connected_nodes.push(new_node);

                }
                println!("added him to the database");
            }
        }
        fn validate_id(str: &str) -> bool {
            return true;
        }

        //================
        //server handshake
        //================
        //validates the user is the delibaratley trying to connect to the network

        //c2s - HANDSHAKE_PHRASE
        //s2c - ok
        //c2s - MY_ID
        //cs2 = ok
        const HANDSHAKE_PHRASE: &str = "rock and stone";

        
        fn client_handshake_protocol(new_socket: &mut TcpStream) -> bool{
            //stage 1
            new_socket.flush().unwrap();
            match new_socket.write_all(P2pListener::HANDSHAKE_PHRASE.as_bytes()) {
                Ok(_) => {},
                Err(_) => {return false},
            };
            //stage 2
            let mut handshake_buffer = String::new();

            match new_socket.read_to_string(&mut handshake_buffer) {
                Ok(_) => {},
                Err(_) => {return false},
            };

            println!("c: {}", handshake_buffer);
            return true;
        }

        fn server_handshake_protocol(new_socket: &mut TcpStream) -> Result<String, &str>{

            //stage 1
            let mut handshake_buffer = String::new();

            match new_socket.read_to_string(&mut handshake_buffer) {
                Ok(_) => {},
                Err(_) => {return Err("s: could not receive the handshake")},
            };

            println!("s: {}", handshake_buffer);
            //stage 2
            new_socket.flush().unwrap();
            match new_socket.write_all(P2pListener::HANDSHAKE_PHRASE.as_bytes()) {
                Ok(_) => {},
                Err(_) => {return Err("c: could not send handshake phrase to server");},
            };
           return Ok("hi".to_string());
        }

    }

    struct P2pNode {
        ip: String,
        stream: TcpStream,
    }

    impl P2pNode {
        fn new(ip: String, stream: TcpStream) -> P2pNode {
            let mut node = P2pNode {ip: ip, stream: stream};    
            node
        }
    }

}

