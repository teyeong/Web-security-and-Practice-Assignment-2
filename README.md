# Web-security-and-Practice-Assignment-2
23-2 웹보안및실습 과제 2
## 요구사항
- 파일 암호화: AES_CBC 128 bits key
- 대칭키의 암호화: RSA 2048 (PKCS#1-OAEP)
## 프로그램 사용 방법
1.	encrypt.py와 decrypt.py 파일이 있는 디렉터리에 .txt 파일을 생성하여 저장한다.
2.	Anaconda prompt를 실행하고 해당 폴더로 이동한 후 가상환경을 활성화한다. <br> ex) `conda activate pr_hybrid`
3.	암호화를 진행한다. `python encrypt.py` 명령어를 실행한다.
4.	복호화를 진행한다. `python decrypt.py` 명령어를 실행한다.
## 암호화 동작 과정
### 키 생성
-	파일을 암호화하는데 사용할 대칭키를 `get_random_bytes(16)`으로 생성한다.
-	대칭키를 암호화할 공개키와 개인키를 RSA를 사용하여 생성한다.
### 모든 텍스트 파일 가져오기
-	`glob.glob('*.txt')`를 이용해 현재 디렉터리에 있는 모든 텍스트 파일을 가져온다.
### 대칭키 암호화
-	대칭키를 RSA 2048(PKCS1_OAEP)를 이용해 공개키로 암호화한다.
-	대칭키는 enc_symmetric_key.bin 파일에 저장한다.
### 텍스트 파일 암호화
-	AES object를 CBC mode로 initiate한다.
-	iv를 based64 encoder로 인코딩 후 따로 파일로 저장한다.
-	현재 텍스트 파일을 읽어서 변수 data에 저장한다.
-	data를 16 bytes size로 pad하고 AES로 암호화한다.
-	암호화한 ct_bytes를 based64 encoder로 인코딩 후 새로운 파일로 저장한다.
## 복호화 동작 과정
### 대칭키 복호화
-	RSA로 암호화한 대칭키를 개인키로 복호화한다.
### 모든 암호화 파일 가져오기
-	`glob.glob('*.enc')`를 사용해서 모든 암호화 파일을 가져온다.
### 암호화 파일 복호화
-	암호화할 때 저장한 iv 파일을 읽어오고 base64로 decode한다.
-	현재 암호화 파일을 읽어오고 base64로 decode한다.
-	대칭키를 사용해서 AES 복호화를 한다.
-	복호화한 ct에서 16 bytes size를 unpad하고 변수 pt에 저장한다.
-	pt를 파일에 쓴다. 이때 원문과 비교하기 위해 파일명 앞에 `dec_`를 붙인다.
