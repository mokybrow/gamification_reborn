"use client"

import Image from "next/image"
import * as user from '@/static/user.png';
import * as searchico from '@/static/searchico.png';
import * as menu from '@/static/menu.png';
import * as home from '@/static/home.png';
import styles from './menu.module.css'
import Link from "next/link";
import { usePathname } from "next/navigation";



const Menu = () => {

    const currentRoute = usePathname();

    return (
        <div className={styles.menu}>
            <div className={styles.menulimit}>
                <button>
                    <Image src={menu} alt={"dev logo"} width={32} height={32} />

                </button>
                <Link href={"/"} className={currentRoute === "/"
                    ? styles.pointermenu
                    : "notpointer"}>
                    <Image src={home} alt={"dev logo"} width={32} height={32} />

                </Link>
                <Link href={"/search"} className={currentRoute === "/search"
                    ? styles.pointermenu
                    : "notpointer"}>
                    <Image src={searchico} alt={"dev logo"} width={32} height={32} />

                </Link>
                <Link href={"/account"} className={currentRoute === "/account"
                    ? styles.pointermenu
                    : "notpointer"}>
                    <Image src={user} alt={"dev logo"} width={32} height={32} />

                </Link>


            </div>
        </div>

    )
}

export default Menu
